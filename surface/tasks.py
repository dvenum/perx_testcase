"""
    celery delayed tasks
"""
from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from celery import shared_task

from storage import models
from surface import processor


@shared_task(ignore_result=True)
def process_document(uuid):
    ''' Obtain results, update model
    '''

    doc_model = models.DocumentModel.objects.get(id=uuid)
    doc_model.status = models.DOCUMENT_STATUS.RUNNING
    doc_model.save()

    doc_processor = processor.Document()
    doc_processor.load_from_model(doc_model)
    x = doc_processor.x
    status = doc_processor.status
    direction = {
        processor.STATUS_ADDED: models.RESULT_DIRECTION.ADDED,
        processor.STATUS_REMOVED: models.RESULT_DIRECTION.REMOVED,
    }.get(status)

    if not direction or x is None or status == processor.STATUS_INVALID:
        doc_model.status = models.DOCUMENT_STATUS.INVALID
        doc_model.save()
        return

    doc_model.status = models.DOCUMENT_STATUS.FINISHED
    doc_model.finished_at = timezone.now()
    doc_model.save()

    result = models.ResultModel(doc_uuid=doc_model, x=x, direction=direction)
    result.save()

