"""Test castle locking."""

from httplib import CREATED, NO_CONTENT, NOT_FOUND, FORBIDDEN
from django.core.urlresolvers import reverse
from django.test import TestCase

from castles.models import Castle
from api.v1.views import SUCCESS, CASTLE_ALREADY_ACQUIRED, CASTLE_ACQUIRED_BY_OTHER_USER
from api.v1.views import CASTLE_NOT_ACQUIRED

CASTLE_IP = "10.10.10.10"
CLIENT_ADDRESS = "172.169.0.123"

def _get_user():
    """Get the owning user of a castle resource."""
    (user, ) = (castle.user for castle in Castle.objects.filter(host = CASTLE_IP))
    return user

class TestLocks(TestCase):
    def setUp(self):
        castle = Castle(host = CASTLE_IP, gatekeeper = "172.168.0.1")
        # pylint: disable=no-member
        castle.save()

        castle.rooms.create(name = "ssh", inside_port = 22, outside_port = 9022)
        castle.rooms.create(name = "ftp", inside_port = 21, outside_port = 9021)

    def test_acquire_nonexistant_castle(self):
        response = self.client.put(reverse("api:v1:lock", args = ("20.20.20.20", )))
        self.assertEqual(NOT_FOUND, response.status_code)

    def test_release_nonexistant_castle(self):
        response = self.client.delete(reverse("api:v1:lock", args = ("20.20.20.20", )))
        self.assertEqual(NOT_FOUND, response.status_code)

    def test_acquire_and_release(self):
        self.assertIsNone(_get_user())

        self.assertTrue(self._acquire())
        self.assertEqual(CLIENT_ADDRESS, _get_user())

        self.assertTrue(self._release())
        self.assertIsNone(_get_user())

    def test_acquire_twice(self):
        self.assertTrue(self._acquire())
        self.assertEqual(CLIENT_ADDRESS, _get_user())

        self.assertEqual(CASTLE_ALREADY_ACQUIRED, self._acquire())
        self.assertEqual(CLIENT_ADDRESS, _get_user())

        self.assertEqual(CASTLE_ALREADY_ACQUIRED, self._acquire("1.2.3.4"))
        self.assertEqual(CLIENT_ADDRESS, _get_user())

    def test_release_other(self):
        self.assertTrue(self._acquire())
        self.assertEqual(CLIENT_ADDRESS, _get_user())

        self.assertEqual(CASTLE_ACQUIRED_BY_OTHER_USER, self._release("1.2.3.4"))
        self.assertEqual(CLIENT_ADDRESS, _get_user())

        self.assertTrue(self._release())
        self.assertIsNone(_get_user())

    def test_release_unacquired(self):
        self.assertEqual(CASTLE_NOT_ACQUIRED, self._release())
        self.assertIsNone(_get_user())

    def _acquire(self, client = None):
        """Send a lock acquire (PUT) request."""
        if not client:
            client = CLIENT_ADDRESS

        response = self.client.put(
            reverse("api:v1:lock", args = (CASTLE_IP, )),
            HTTP_X_FORWARDED_FOR = client)

        content = response.json()
        self.assertEqual(CASTLE_IP, content["castle"])

        if FORBIDDEN == response.status_code:
            return content["code"]

        self.assertEqual(CREATED, response.status_code)
        self.assertEqual(reverse("api:v1:show", args = (CASTLE_IP, )), response["Location"])
        self.assertEqual(SUCCESS, content["code"])
        return True

    def _release(self, client = None):
        """Send a lock release (DELETE) request."""
        if not client:
            client = CLIENT_ADDRESS

        response = self.client.delete(
            reverse("api:v1:lock", args = (CASTLE_IP, )),
            HTTP_X_FORWARDED_FOR = client)

        if FORBIDDEN == response.status_code:
            content = response.json()
            self.assertEqual(CASTLE_IP, content["castle"])
            return content["code"]

        self.assertEqual(NO_CONTENT, response.status_code)
        return True
