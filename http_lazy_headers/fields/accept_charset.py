# -*- coding: utf-8 -*-

from ..shared.values import charsets
from ..shared import bases


def accept_charset(charset, quality=None):
    assert (
        charset == '*' or
        charset in charsets.CHARSET_VALUES)
    assert (
        quality is None or
        0 <= quality <= 1)

    return charset, quality


class AcceptCharset(bases.AcceptSomeBase):
    """
    Sent by client only.

    The Accept-Charset header field can be\
    sent by a user agent to indicate what\
    charsets are acceptable in textual response\
    content. This field allows user agents\
    capable of understanding more comprehensive\
    or special-purpose charsets to signal that\
    capability to an origin server that is capable\
    of representing information in those charsets.

    Example::

        AcceptCharset([
            accept_charset(Charset.utf_8, quality=1),
            accept_charset('*', quality=0.5)
        ])

        AcceptCharset([
            ('iso-8859-5', None),
            ('unicode-1-1', 0.8)
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.accept-charset>`_
    """

    name = 'accept-charset'
