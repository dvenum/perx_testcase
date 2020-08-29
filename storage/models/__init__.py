""" 
    usage:
        from storage import models
        models.Company
"""
import os

from core import settings

"""
# when we use db models from cmd-line access points, we should configure django AppRegistry
# Ray lib run it again
import sys
from django.apps import apps
if not (sys.argv[0].endswith('manage.py') or sys.argv[0].endswith('/gunicorn') or apps.ready):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    import django
    django.setup()
"""

