# -*- coding: utf-8 -*-

from ..shared.common import hosts
from ..shared.utils import assertions
from ..shared.utils import constraints
from ..shared.utils import parsers
from .. import exceptions
from ..shared import bases


def via(
        version,
        protocol=None,
        host=None,
        pseudonym=None,
        comment=None):
    assert host or pseudonym
    assert not (host and pseudonym)

    return (
        (protocol, version),
        (host or hosts.host(), pseudonym),
        comment)


class Via(bases.MultiHeaderBase):
    """
    The ``Via`` header field indicates the\
    presence of intermediate protocols and\
    recipients between the user agent and the\
    server (on requests) or between the origin\
    server and the client (on responses),\
    similar to the "Received" header field in\
    email. Via can be used for tracking message\
    forwards, avoiding request loops, and\
    identifying the protocol capabilities of\
    senders along the request/response chain.

    Example::

        Vary([
            via(
                version='1.0',
                pseudonym='fred',
                comment='middle man'),
            via(
                version='1.1',
                host=host('p.example.net')])

    `Ref. <http://httpwg.org/specs/rfc7230.html#header.via>`_
    """

    name = 'via'

    def check_one(self, value):
        assertions.must_be_tuple_of(value, 3)
        assertions.must_be_tuple_of(value[0], 2)
        assertions.must_be_tuple_of(value[1], 2)

        (protocol, version), (host, pseudonym), comment = value

        protocol is None or assertions.must_be_token(protocol)
        assertions.must_be_token(version)
        assertions.assertion(
            (pseudonym and
             host == hosts.host()) or
            (not pseudonym and
             host != hosts.host()),
            '"{}" and "{}" received, either '
            'pseudonym or host was expected'
            .format(pseudonym, host))
        pseudonym is None or assertions.must_be_token(pseudonym)
        hosts.check_host(host)
        comment is None or assertions.must_be_ascii(comment)

    def to_str_one(self, value):
        (protocol, version), (host, pseudonym), comment = value

        proto = version

        if protocol is not None:
            proto = '/'.join((protocol, version))

        received_by = pseudonym or hosts.format_host(host)

        if comment is not None:
            return "{} {} {}".format(
                proto,
                received_by,
                parsers.quote_comment(comment))
        else:
            return "{} {}".format(
                proto,
                received_by)

    def to_str(self, values):
        return ', '.join((
            self.to_str_one(value)
            for value in values))

    def clean_one(self, raw_value):
        try:
            version, received_by = raw_value.split(' ', 1)
        except ValueError:
            raise exceptions.BadRequest(
                'Expected "protocol received_by" format')

        try:
            protocol, version = version.split('/', 1)
        except ValueError:
            protocol = None
        else:
            constraints.must_be_token(protocol)

        constraints.must_be_token(version)

        try:
            received_by, comment = received_by.split(' ', 1)
        except ValueError:
            comment = None
        else:
            constraints.must_be_comment(comment)
            comment = parsers.dequote_comment(comment)

        try:
            host = hosts.clean_host(received_by)
        except exceptions.HeaderError:
            constraints.must_be_token(received_by)
            pseudonym = received_by
            host = hosts.host()
        else:
            pseudonym = None

        return (
            (protocol, version),
            (host, pseudonym),
            comment)
