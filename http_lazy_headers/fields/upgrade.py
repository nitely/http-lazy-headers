# -*- coding: utf-8 -*-

from ..shared.utils import constraints
from ..shared.utils import assertions
from ..shared import bases


def upgrade(name, version=None):
    return name, version


class ProtocolOptions:

    # http://www.iana.org/assignments/http-upgrade-tokens/http-upgrade-tokens.xml

    http = 'HTTP'
    tls = 'TLS'
    web_socket = 'WebSocket'
    h2c = 'h2c'


class Upgrade(bases.MultiHeaderBase):
    """
    The ``Upgrade`` header field is intended to\
    provide a simple mechanism for transitioning\
    from HTTP/1.1 to some other protocol on the\
    same connection. A client MAY send a list of\
    protocols in the Upgrade header field of a\
    request to invite the server to switch to\
    one or more of those protocols, in order of\
    descending preference, before sending the\
    final response. A server MAY ignore a\
    received Upgrade header field if it wishes\
    to continue using the current protocol on\
    that connection. Upgrade cannot be used to\
    insist on a protocol change.

    Example::

        Upgrade([
            upgrade(ProtocolName.http, '2.0')
        ])

        Upgrade([
            upgrade(ProtocolName.web_socket)
        ])

        Upgrade([
            ('HTTP', '2.0'),
            ('SHTTP', '1.3'),
            ('IRC', '6.9'),
            ('RTA', 'x11')
        ])

    `Ref. <http://httpwg.org/specs/rfc7230.html#header.upgrade>`_
    """

    name = 'upgrade'

    def check_value(self, value):
        assertions.must_be_tuple_of(value, 2)
        protocol, version = value
        assertions.must_be_token(protocol)
        version is None or assertions.must_be_token(version)

    def value_str(self, value):
        protocol, version = value

        if version:
            return '{}/{}'.format(protocol, version)

        return protocol

    def values_str(self, values):
        return ', '.join(
            self.value_str(v)
            for v in values)

    def clean_value(self, raw_value):
        try:
            protocol_name, protocol_version = raw_value.split('/', 1)
        except ValueError:
            constraints.must_be_token(raw_value)  # Just name
            return raw_value, None
        else:
            constraints.must_be_token(protocol_name)
            constraints.must_be_token(protocol_version)
            return protocol_name, protocol_version
