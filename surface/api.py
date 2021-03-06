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
from rest_framework.permissions import IsAuthenticated

#from django.db.models import Func, F, Q

import core.utils
from core import settings
from core import logs
from surface import serializers, rest
from storage import models
from surface import tasks

logger = logs.get_logger(__name__)

 
class document_upload(APIView):
    parser_classes = [FileUploadParser]
    permission_classes = [IsAuthenticated]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']

        if not core.utils.validate_excel(file_obj):
            return Response({f'{filename}': '', 
                              'error': 'wrong format. xlsx/xls allowed only.'})

        document = models.DocumentModel(
                located=models.DOCUMENT_LOCATION.LOCAL,
        )
        if document.store(file_obj):
            # write to file storage
            document.save()

            # put document to queue
            tasks.process_document.delay(document.id)
            #tasks.process_document(document.id)

            return Response({f'{filename}': f'{document.id}',
                              'error': 'ok'})
        else:
            return Response({f'{filename}': '', 
                              'error': 'Service unavailable.'})


class get_status(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        doc_model = models.DocumentModel.objects.get(id=uuid)
        if not doc_model:
            return Response({'status': 'unknown',
                             'error': 'unknown uuid'})

        if doc_model.status == models.DOCUMENT_STATUS.FINISHED:
            result = models.ResultModel.objects.get(doc_uuid=uuid)
            if not result:
                return Response({'status': 'finished',
                                 'uploaded_at': doc_model.uploaded_at,
                                 'error': 'unknown result'})

            return Response({'status': 'finished',
                             'uploaded_at': doc_model.uploaded_at,
                             'finished_at': doc_model.finished_at,
                             'result': f'{result.direction.label}: {result.x}',
                             'error': 'ok'})
        else:
            return Response({'status': {'P': 'pending', 'R': 'running'}.get(doc_model.status.label, 'unknown'),
                             'uploaded_at': doc_model.uploaded_at,
                             'error': 'ok'})

