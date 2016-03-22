"""API v1 Views."""

from httplib import CREATED, NO_CONTENT, FORBIDDEN
from django.utils.timezone import now
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic import View

from castles.models import Castle

(SUCCESS,
 CASTLE_ALREADY_ACQUIRED,
 CASTLE_NOT_ACQUIRED,
 CASTLE_ACQUIRED_BY_OTHER_USER,
) = range(4)

MESSAGES = {
    SUCCESS: "Success",
    CASTLE_ALREADY_ACQUIRED: "Castle is already acquired",
    CASTLE_NOT_ACQUIRED: "Castle is not acquired",
    CASTLE_ACQUIRED_BY_OTHER_USER: "Castle acquired by another user",
}

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

@method_decorator(csrf_exempt, name = "dispatch")
@method_decorator(atomic, name = "dispatch")
class LockView(View):
    """Manage a lock on a castle resource."""
    @staticmethod
    def put(request, host):
        """Acquire lock via PUT."""
        castle = get_object_or_404(Castle, host = host)

        if castle.user:
            return _build_reponse(FORBIDDEN, CASTLE_ALREADY_ACQUIRED, castle)

        castle.taken_at = now()
        castle.user = _get_client_ip(request)
        castle.save()

        response = _build_reponse(CREATED, SUCCESS, castle)
        response["Location"] = reverse("api:v1:show", args = (castle.host, ))
        return response

    @staticmethod
    def delete(request, host):
        """Release lock via DELETE."""
        castle = get_object_or_404(Castle, host = host)

        if not castle.user:
            return _build_reponse(FORBIDDEN, CASTLE_NOT_ACQUIRED, castle)

        if castle.user != _get_client_ip(request):
            return _build_reponse(FORBIDDEN, CASTLE_ACQUIRED_BY_OTHER_USER, castle)

        castle.taken_at = None
        castle.user = None
        castle.save()

        return HttpResponse(status = NO_CONTENT)

def _build_reponse(status, code, castle):
    """Build a generic json response to a REST action."""
    return JsonResponse(
        {"code": code, "message": MESSAGES[code], "castle": castle.host, },
        status = status)

def _get_client_ip(request):
    """Resolve the client's IP from the HTTP request."""
    client_ip = request.META.get("HTTP_X_FORWARDED_FOR")
    if client_ip:
        return client_ip

    return request.META.get("REMOTE_ADDR")
