# -*- coding: utf-8 -*-

from ..shared import bases


def vary_any():
    return '*'


class Vary(bases.TokensHeaderBase):
    """
    Sent by server only.

    The ``Vary`` header field in a response\
    describes what parts of a request message,\
    aside from the method, Host header field,\
    and request target, might influence the\
    origin server's process for selecting and\
    representing this response. The value consists\
    of either a single asterisk ("*") or a list\
    of header field names (case-insensitive).

    Example::

        Vary([
            'accept-encoding',
            'accept-language'
        ])

        Vary([
            vary_any()
        ])

        Vary(['*'])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.vary>`_
    """

    name = 'vary'

    # todo: validate is a single * value or a list of headers
