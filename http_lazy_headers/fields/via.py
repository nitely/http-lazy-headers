# -*- coding: utf-8 -*-

from .. import exceptions
from ..shared import bases
from ..shared import checkers
from ..shared import constraints
from ..shared import parsers


def via(received_protocol, received_by, comment=None):
    return received_protocol, received_by, comment


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
                received_protocol='1.0',
                received_by='fred',
                comment='middle man'),
            via(
                received_protocol='1.1',
                received_by='p.example.net'])

    `Ref. <http://httpwg.org/specs/rfc7230.html#header.via>`_
    """

    name = 'via'

    def value_str(self, value):
        protocol, received_by, comment = value

        if comment is not None:
            return "{} {} {}".format(
                protocol,
                received_by,
                parsers.quote_comment(comment))
        else:
            return "{} {}".format(
                protocol,
                received_by)

    def values_str(self, values):
        return ', '.join((
            self.value_str(value)
            for value in values))

    def clean_value(self, raw_value):
        try:
            protocol, received_by = raw_value.split(' ', 1)
        except ValueError:
            raise exceptions.BadRequest(
                'Expected "protocol received_by" format')

        try:
            protocol_name, protocol_version = raw_value.split('/', 1)
        except ValueError:
            constraints.must_be_token(protocol)  # Just version
        else:
            constraints.must_be_token(protocol_name)
            constraints.must_be_token(protocol_version)

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

        return protocol, received_by, comment
