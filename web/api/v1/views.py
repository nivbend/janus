"""API v1 Views."""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from castles.models import Castle

@csrf_exempt
def show(_, host):
    """Return a castle resource by its hostname."""
    castle = get_object_or_404(Castle, host = host)
    return JsonResponse({
        "host": castle.host,
        "gatekeeper": castle.gatekeeper,
        "rooms": [(room.outside_port, room.inside_port) for room in castle.rooms.all()],
        "user": castle.user,
    })
