"""Castles URL Configuration

These pages are the front-end of the application, aggregating information and displaying it in a
pretty fashion."""

from django.conf.urls import url

from .views import CastlesList

app_name = 'castles'

urlpatterns = [
    url(r'^$', CastlesList.as_view(), name = 'all'),
]
