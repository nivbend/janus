"""Manage connections between clients and the "castle" (remote resource)."""

from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from SocketServer import ThreadingTCPServer
from abc import ABCMeta, abstractmethod

from .forward import ForwardingHandler

class Gate(ThreadingTCPServer, object):
    """Guard a connection between a "room" in a "castle" (server port on a resource).

    A gate is a server which connects the tunnel for each incoming connection.
    """
    __metaclass__ = ABCMeta
    allow_reuse_address = True

    def __init__(self, outer_port, castle_host, room_port):
        super(Gate, self).__init__(("", outer_port), ForwardingHandler)
        self.__castle_host = castle_host
        self.__room_port = room_port
        self.__inner_socket = None

    @property
    def room_address(self):
        """Return the room's address (castle:inner_port)."""
        return (self.__castle_host, self.__room_port)

    def process_request(self, request, client_address):
        assert self.__inner_socket is None
        self.__inner_socket = self._open_gate()
        super(Gate, self).process_request(request, client_address)

    def finish_request(self, request, client_address):
        # Passing the channel as the target of the forwarding handler.
        class Handler(self.RequestHandlerClass):
            # pylint: disable=missing-docstring, no-init, too-few-public-methods
            target = self.__inner_socket

        Handler(request, client_address, self)

    def close_request(self, request):
        self.__inner_socket.close()
        self.__inner_socket = None
        request.close()

    @abstractmethod
    def _open_gate(self):
        """Open the gate - essentially connecting to the room's port on the castle resource."""
        return None

    def __str__(self):
        (_, outer_port) = self.server_address
        return "%s(%d <-> %s:%d)" % (
            self.__class__.__name__,
            outer_port,
            self.__castle_host,
            self.__room_port,
        )

class TCPGate(Gate):
    """A gate connecting via TCP."""
    def _open_gate(self):
        inner_socket = socket(AF_INET, SOCK_STREAM)
        inner_socket.connect(self.room_address)
        return inner_socket

class UDPGate(Gate):
    """A gate connecting via UDP."""
    def _open_gate(self):
        inner_socket = socket(AF_INET, SOCK_DGRAM)
        inner_socket.connect(self.room_address)
        return inner_socket
