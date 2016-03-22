# pylint: disable=missing-docstring
from django.contrib.admin import ModelAdmin, register

from castles.models import Castle, Room

@register(Room)
class RoomAdmin(ModelAdmin):
    pass

@register(Castle)
class CastleAdmin(ModelAdmin):
    list_display = ('host', 'gatekeeper', 'room_count')

    @staticmethod
    def room_count(castle):
        return castle.rooms.count()
