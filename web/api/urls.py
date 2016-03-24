"""API URL Configuration

Routing to different version is performed here. 'latest' will always redirect to the most recent
API version.
"""

from django.conf.urls import url, include
from django.views.generic import RedirectView

app_name = 'api'

urlpatterns = [
    url(r'^latest/(?P<path>.*)$', RedirectView.as_view(url = '/api/1/%(path)s'), name = 'latest'),
    url(r'^1/', include('api.v1.urls', namespace = 'v1')),
]
