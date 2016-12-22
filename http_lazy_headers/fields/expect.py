# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import constraints


_CONTINUE = '100-continue'


def expect_continue():
    return _CONTINUE


class Expect(bases.SingleHeaderBase):
    """
    Sent by client only.

    The ``Expect`` header field in a request\
    indicates a certain set of behaviors\
    (expectations) that need to be supported\
    by the server in order to properly handle\
    this request.

    Example::

        Expect([
            expect_continue()
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.expect>`_
    """

    name = 'expect'

    def clean_value(self, raw_value):
        constraints.constraint(
            raw_value == _CONTINUE,
            '{} is not a valid value'.format(raw_value),
            status=417)
        return raw_value
