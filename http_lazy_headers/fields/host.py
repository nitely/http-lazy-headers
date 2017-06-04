# -*- coding: utf-8 -*-

from ..shared.common import hosts
from ..shared.utils import constraints
from ..shared import bases


class Host(bases.SingleHeaderBase):
    """
    Sent by client only

    This field may be empty.

    This will validate the ``format`` for port,\
    domain, ipv4, ipv6, ipvFuture and unsafe host.\
    However, that does not mean that the value\
    is actually valid.

    Make sure to check the value against a\
    white-list of valid domains. Search for\
    "host poisoning" for examples of what\
    may happen failing to do that.

    The ``Host`` header field in a request\
    provides the host and port information\
    from the target URI, enabling the origin\
    server to distinguish among resources\
    while servicing requests for multiple\
    host names on a single IP address.

    Example::

        # Empty host
        Host([
            host()
        ])

        Host([
            host('example.org')
        ])

        Host([
            host('example.org', port=8000)
        ])

        Host([
            host('www.Alliancefrançaise.nu')
        ])

        Host([
            host(ipv4='123.123.123.123')
        ])

        Host([
            host(ipv6='2001:db8:a0b:12f0::1')
        ])

        Host([
            host(ipv_future='v0.01:77:00:00:00:01')
        ])

    `Ref. <http://httpwg.org/specs/rfc7230.html#header.host>`_
    """

    name = 'host'

    def check_one(self, value):
        hosts.check_host(value)

    def to_str(self, values):
        return hosts.format_host(values[0])

    def clean_one(self, raw_value):
        return hosts.clean_host(raw_value)

    def clean(self, raw_values):
        # Allow empty value
        constraints.constraint(
            len(raw_values) == 1,
            'Header must have one '
            'value and be unique',
            status=400)
        raw_value = raw_values[0].strip()

        if raw_value:
            return (
                self.clean_one(raw_value),)
        else:
            return (
                hosts.host(),)
