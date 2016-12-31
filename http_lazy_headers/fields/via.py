# -*- coding: utf-8 -*-

from ..shared.utils import assertions
from ..shared.utils import checkers
from ..shared.utils import constraints
from ..shared.utils import parsers
from .. import exceptions
from ..shared import bases


def via(version, received_by, protocol=None, comment=None):
    return (protocol, version), received_by, comment


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
                received_by='fred',
                comment='middle man'),
            via(
                version='1.1',
                received_by='p.example.net'])

    `Ref. <http://httpwg.org/specs/rfc7230.html#header.via>`_
    """

    name = 'via'

    # todo: validate received_by as host
    # todo: should be (received_by_host, received_by_port)

    def check_value(self, value):
        assertions.must_be_tuple_of(value, 3)
        assertions.must_be_tuple_of(value[0], 2)

        (protocol, version), received_by, comment = value

        protocol is None or assertions.must_be_token(protocol)
        assertions.must_be_token(version)
        assertions.assertion(
            (checkers.is_uri(received_by) or
             checkers.is_token(received_by)),
            '"{}" received, value received_by '
            'was expected'.format(received_by))
        comment is None or assertions.must_be_ascii(comment)

    def value_str(self, value):
        (protocol, version), received_by, comment = value

        proto = version

        if protocol is not None:
            proto = '/'.join((
                protocol, version))

        if comment is not None:
            return "{} {} {}".format(
                proto,
                received_by,
                parsers.quote_comment(comment))
        else:
            return "{} {}".format(
                proto,
                received_by)

    def values_str(self, values):
        return ', '.join((
            self.value_str(value)
            for value in values))

    def clean_value(self, raw_value):
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

        constraints.constraint(
            (checkers.is_uri(received_by) or
             checkers.is_token(received_by)),
            'The receiver value is not valid')

        return (protocol, version), received_by, comment
