# pylint: disable=missing-docstring

from django.conf.urls import url

from .views import LockView, show

urlpatterns = [
    url(r'^castles/(?P<host>[a-zA-Z0-9_.]+)$', show, name = 'show'),
    url(r'^castles/(?P<host>[a-zA-Z0-9_.]+)/lock$', LockView.as_view(), name = 'lock'),
]
