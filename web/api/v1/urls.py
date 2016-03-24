# pylint: disable=missing-docstring

from django.conf.urls import url

from .views import show

urlpatterns = [
    url(r'^castles/(?P<host>[a-zA-Z0-9_.]+)$', show, name = 'show'),
]
