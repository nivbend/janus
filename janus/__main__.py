"""Package's entry-point."""

from argparse import ArgumentParser, Action
from collections import namedtuple
from .gate import Gate

SSH_PORT = 22

class Host(namedtuple("Host", ["host", "port", "username", ])):
    """A host address, holding its IP, port number and username."""
    def __str__(self):
        hostname = "%s:%d" % (self.host, self.port, )

        if self.username:
            hostname = "%s@%s" % (self.username, hostname, )

        return "%s(%s)" % (self.__class__.__name__, hostname, )

class ParseHost(Action):
    """A host parsing action, converts [username@]host[:port] values to a namedtuple."""
    # pylint: disable=too-few-public-methods
    def __call__(self, parser, namespace, hostname, option_string = None):
        try:
            if ":" in hostname:
                (hostname, port) = hostname.rsplit(":", 2)
            else:
                port = SSH_PORT

            if "@" in hostname:
                (username, hostname) = hostname.split("@", 2)
            else:
                username = None
        except ValueError:
            raise ValueError("Invalid hostname: %s" % (hostname, ))

        setattr(namespace, self.dest, Host(hostname, int(port), username))

def _parse_arguments():
    # pylint: disable=missing-docstring
    parser = ArgumentParser(
        description = "Create an SSH tunnel")

    parser.add_argument(
        "gate_port",
        metavar = "port",
        type = int,
        help = "Gatekeeper port for incoming connections")

    parser.add_argument(
        "castle",
        action = ParseHost,
        help = "Castle's address ([username@]host[:port])")

    return parser.parse_args()

def run():
    """Package's entry-point."""
    arguments = _parse_arguments()

    gate = Gate(
        arguments.gate_port,
        arguments.castle.host,
        arguments.castle.port)

    print "Now forwarding port %d to remote %s" % (arguments.gate_port, arguments.castle, )
    try:
        gate.serve_forever()
    except KeyboardInterrupt:
        print "C-c: Port forwarding stopped."

    return 0

if __name__ == "__main__":
    exit(run())
