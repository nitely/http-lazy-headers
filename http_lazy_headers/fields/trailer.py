# -*- coding: utf-8 -*-

from ..shared import bases


class Trailer(bases.TokensHeaderBase):
    """
    When a message includes a message body encoded\
    with the chunked transfer coding and the sender\
    desires to send metadata in the form of trailer\
    fields at the end of the message, the sender\
    SHOULD generate a ``Trailer`` header field before\
    the message body to indicate which fields will\
    be present in the trailers. This allows the\
    recipient to prepare for receipt of that\
    metadata before it starts processing the body,\
    which is useful if the message is being\
    streamed and the recipient wishes to confirm\
    an integrity check on the fly.

    Example::

        Trailer([
            'CRC32',
            ContentLength.name
        ])

    `Ref. <http://httpwg.org/specs/rfc7230.html#header.trailer>`_
    """

    name = 'trailer'
