from django.urls import include, path, re_path
from rest_framework import routers
from surface import api
from surface import views

router = routers.DefaultRouter()

app_name = 'surface'

urlpatterns = [
    #path('api/', include(router.urls)),
    re_path('^upload/(?P<filename>[^/]+)$', api.document_upload.as_view(), name='upload'),
    re_path('^status/(?P<uuid>.+)$', api.get_status.as_view(), name='status'),
]
