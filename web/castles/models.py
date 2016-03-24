# pylint: disable=missing-docstring
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db.models import Model
from django.db.models import (ManyToManyField, CharField, DateTimeField, GenericIPAddressField,
                              PositiveSmallIntegerField)

@python_2_unicode_compatible
class Room(Model):
    created = DateTimeField(auto_now_add = True)
    last_modified = DateTimeField(auto_now = True)
    name = CharField(max_length = 20, blank = True, unique = True)
    inside_port = PositiveSmallIntegerField('room_port', default = 22)
    outside_port = PositiveSmallIntegerField('gate_port', default = 9022)

    def __str__(self):
        if not self.name:
            return '{:d}<->{:d}'.format(self.outside_port, self.inside_port)

        return '{:s} ({:d}<->{:d})'.format(self.name, self.outside_port, self.inside_port)

@python_2_unicode_compatible
class Castle(Model):
    created = DateTimeField(auto_now_add = True)
    last_modified = DateTimeField(auto_now = True)
    host = GenericIPAddressField(protocol = 'IPv4', default = '0.0.0.0', unique = True)
    alias = CharField(max_length = 20, blank = True, unique = True)
    gatekeeper = GenericIPAddressField(protocol = 'IPv4', default = '0.0.0.0', unique = True)
    rooms = ManyToManyField(Room)
    user = GenericIPAddressField(protocol = 'IPv4', null = True, blank = True, editable = False)
    taken_at = DateTimeField(null = True, editable = False)

    def __str__(self):
        if not self.user:
            return '{:s} (behind {:s})'.format(self.host, self.gatekeeper)

        return '{:s} (behind {:s}, aqcuired by {:s})'.format(self.host, self.gatekeeper, self.user)
