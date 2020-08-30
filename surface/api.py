"""
"""

import json

#from django.shortcuts import redirect
#from django.core.serializers.json import DjangoJSONEncoder
#import django_filters.rest_framework
#from django.http import HttpResponse
#from django.http import StreamingHttpResponse
#from rest_framework import viewsets, generics
from rest_framework.response import Response
#from rest_framework import filters
#from rest_framework.decorators import action

from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

#from django.db.models import Func, F, Q

import core.utils
from core import settings
from core import logs
from surface import serializers, rest
from storage import models

logger = logs.get_logger(__name__)

 
class document_upload(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']

        if not core.utils.validate_excel(file_obj):
            return Response({f'{filename}': '', 
                              'Error': 'wrong format. xlsx/xls allowed only.'})

        document = models.DocumentModel(
                located=models.DOCUMENT_LOCATION.LOCAL,
        )
        if document.store(file_obj):
            document.save()
            fobj = document.load()
            return Response({f'{filename}': f'{document.id}'})
        else:
            return Response({f'{filename}': '', 
                              'Error': 'Service unavailable.'})

