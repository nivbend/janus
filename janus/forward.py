"""Define a request handler which forwards packets to/from the request and the channel."""

from select import select
from SocketServer import BaseRequestHandler

class ForwardingHandler(BaseRequestHandler, object):
    """Forward packets between the request and a given target.

    The target attribute should be defined before instantiating a ForwardingHandler (since the
    BaseRequestHandler's constructor calls `handle()`). This could be achieved by dynamically
    sub-classing this class:
    >>> def finish_request(request, client_address): # doctest: +SKIP
    ...     class Handler(ForwardingHandler):
    ...         target = <something socket-like>
    ...     Handler(request, client_address, self)
    """
    def setup(self):
        if not hasattr(self, "target"):
            raise ValueError("Must define 'target'")

    def handle(self):
        # pylint: disable=no-member
        while True:
            (readable, _, _) = select([self.request, self.target, ], [], [])

            if self.request in readable:
                data = self.request.recv(1024)
                if not data:
                    break

                self.target.send(data)

            if self.target in readable:
                data = self.target.recv(1024)
                if not data:
                    break

                self.request.send(data)
