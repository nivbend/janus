"""Pretty castles views."""

from django.views.generic import ListView

from .models import Castle

class CastlesList(ListView):
    """Show all castles and their states in a pretty table."""
    # pylint:disable=too-many-ancestors
    model = Castle
    template_name = "castles/all.html"
    context_object_name = "castles"
