"""

"""

import django
from django.utils import timezone
from django.conf import settings
from django.db import models, transaction, connections
from django.db.models import QuerySet, Manager

from distutils.version import LooseVersion
DJANGO_VERSION_GTE_19 = LooseVersion(django.get_version()) \
                        >= LooseVersion('1.9')

from core import consts


class TimestampMixin(models.Model):
    """ Timestamp mixin that adds default created_at and updated_at fields
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FuzzyCountQuerySet(QuerySet):
    ''' Usage:
        class Artist(db.Models):
            objects = FuzzyCountQuerySet()
            ..
    '''

    def count(self):
        ''' Take count from pg_class table, if WHERE exists on query,
            it use database function count_estimate() and it should be exists

            config/postgresql/init.sql:
            CREATE OR REPLACE FUNCTION count_estimate(query text) RETURNS INTEGER AS
            $func$
            DECLARE
                rec   record;
                ROWS  INTEGER;
            BEGIN
                FOR rec IN EXECUTE 'EXPLAIN ' || query LOOP
                    ROWS := SUBSTRING(rec."QUERY PLAN" FROM ' rows=([[:digit:]]+)');
                    EXIT WHEN ROWS IS NOT NULL;
                END LOOP;
            
                RETURN ROWS;
            END
            $func$ LANGUAGE plpgsql;
        '''

        # when filter applied by id, we have not too much rows and can count them as is
        # this is important to see correct pagination or we loose last few pages
        sql_str = str(self.query)
        if 'WHERE' in sql_str:
            filter_part = sql_str.split('WHERE')[1]
            if '_id' in filter_part:
                return super(FuzzyCountQuerySet, self).count()

        postgres_engines = ("postgis", "postgresql", "django_postgrespool")
        engine = settings.DATABASES[self.db]["ENGINE"].split(".")[-1]
        is_postgres = engine.startswith(postgres_engines)

        # In Django 1.9 the query.having property was removed and the
        # query.where property will be truthy if either where or having
        # clauses are present. In earlier versions these were two separate
        # properties query.where and query.having
        if DJANGO_VERSION_GTE_19:
            is_filtered = self.query.where
        else:
            is_filtered = self.query.where or self.query.having
        if not is_postgres:
            return super(FuzzyCountQuerySet, self).count()
        cursor = connections[self.db].cursor()
        if is_filtered:
            ''' Working around django bug, it has no quotes for listed items:
                AND "storage_company"."bb_country_code" IN (AV)-> it should be 'AV' here
                It affect only queries, rendered as text, 
            '''
            sql, params = self.query.sql_with_params()
            params = tuple([f"'{p}'" if isinstance(p, str) else p for p in params])
            sql_query = sql % params
            cursor.execute(f"SELECT count_estimate($${sql_query}$$)")
        else:
            cursor.execute("SELECT reltuples FROM pg_class "
                           f"WHERE relname = '{self.model._meta.db_table}';")

        # if not too much rows on result, normal count() is fast enough
        approximate_count = int(cursor.fetchone()[0])
        if approximate_count < consts.DB_APPROXIMATION_COUNT_THRESHOLD:
            return super(FuzzyCountQuerySet, self).count()
        return approximate_count


FuzzyCountManager = Manager.from_queryset(FuzzyCountQuerySet)
