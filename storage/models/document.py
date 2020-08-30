"""
    Define model of xlsx document and related models

"""

#from caching.base import CachingManager, CachingMixin

import uuid
import os


# Dirty hack for testcase only.
# Django 3.1+ has this method moved to public -- https://docs.djangoproject.com/en/3.1/releases/3.1/
# And enumfield lib updating slowly. Normally, it should be patched, forked or replaced (prefer)
import django.utils
django.utils.decorators.classproperty = django.utils.functional.classproperty
from django_enumfield import enum


from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from . import base
from storage import misc
from core import utils, logs
from core import settings

logger = logs.get_logger(__name__)


class DOCUMENT_STATUS(enum.Enum):
    PENDING = 1
    RUNNING = 2
    INVALID = 3
    FINISHED = 4

    __labels__ = {
        PENDING: 'P',
        RUNNING: 'R',
        INVALID: 'I',
        FINISHED: 'F',
    }

    __transitions__ = {
        RUNNING: (PENDING,),
        INVALID: (RUNNING,PENDING),
        FINISHED: (RUNNING,),
    }


class DOCUMENT_LOCATION(enum.Enum):
    LOCAL = 1   # uploaded to MEDIA_ROOT

    __labels__ = {
        LOCAL: 'L',
    }


class RESULT_DIRECTION(enum.Enum):
    ADDED = 1
    REMOVED = 2

    ''' 'Unknown' label is not needed here by performance reason.
        So, we can safely cache result models and keep it minimal volume.
    '''

    __labels__ = {
        ADDED: 'added',
        REMOVED: 'removed',
    }


class DocumentModel(base.TimestampMixin, models.Model):
    """ One uploaded xls/xlsx document
    """
    objects = base.FuzzyCountManager()  # show fast, but delayed amount

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    located = enum.EnumField(DOCUMENT_LOCATION)
    status = enum.EnumField(DOCUMENT_STATUS, default=DOCUMENT_STATUS.PENDING)

    # created_at/updated_at is related to database record
    # uploaded_at/finished_at controling by filehandler
    uploaded_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)

    @property
    def filename(self):

        # extension is not matter here and we set 'xlsx' only to tell humans, 
        # what is on this folder
        if self.located == DOCUMENT_LOCATION.LOCAL:
            return os.path.join(settings.MEDIA_ROOT, f'{self.id}.xlsx')
        return None

    def store_local(self, fobj):
        try:
            with default_storage.open(self.filename, 'wb+') as destination:
                for chunk in fobj.chunks():
                    destination.write(chunk)
        except Exception as e:
            logger.error(repr(e))
            return False
        return True

    def store(self, fobj):
        ''' write to file storage
        '''
        if self.located == DOCUMENT_LOCATION.LOCAL:
            return self.store_local(fobj)
        return None

    def load(self):
        ''' return file object
        '''
        try:
            fobj = open(self.filename, 'rb')
        except Exception as e:
            logger.error(repr(e))
            return None
        return fobj

    def __str__(self):
        return f'{self.id} {self.located.label} {self.filename}'

    class Meta:
        base_manager_name = 'objects'
        indexes = [
            models.Index(fields=['status'], name='status_idx'),
        ]


class ResultModel(base.TimestampMixin, models.Model):
    """ Documents processed data

        Note: С немалой вероятностью, информации будет больше со временем.
              И использоваться она будет чаще, чем сам документ, поэтому отдельная таблица,
              которая на начальном этапе выглядит ненужной.
    """
    #objects = CachingManager()
    doc_uuid = models.ForeignKey('DocumentModel', on_delete=models.CASCADE,
                                            null=False, blank=False)
    x = models.FloatField(null=True, blank=False)
    direction = enum.EnumField(RESULT_DIRECTION)

    def __str__(self):
        return f'{self.direction.label}: {self.x}'

    class Meta:
        base_manager_name = 'objects'
        indexes = [
            models.Index(fields=['direction'], name='direction_idx'),
            models.Index(fields=['doc_uuid'], name='doc_uuid_idx'),
            models.Index(fields=['direction', 'doc_uuid'], name='direction_uuid_idx'),
        ]
    
