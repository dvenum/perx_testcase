""" 
    usage:
        from storage import models
        models.Company
"""
import os

from core import settings


from .document import (
    DocumentModel,
    ResultModel,
    DOCUMENT_LOCATION,
)

