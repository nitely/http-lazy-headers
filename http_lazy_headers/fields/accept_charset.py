# -*- coding: utf-8 -*-

from ..shared.utils import assertions
from ..shared.values import charsets
from ..shared import bases
from ..shared import parameters


def accept_charset(charset, quality=None):
    assert (
        charset == '*' or
        charset in charsets.CHARSET_VALUES)
    assert (
        quality is None or
        0 <= quality <= 1)

    params = ()

    if quality is not None:
        params = (('q', quality),)

    return charset, parameters.ParamsCI(params)


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
            ('iso-8859-5', Params()),
            ('unicode-1-1', Params({'q': 0.8}))
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.accept-charset>`_
    """

    name = 'accept-charset'

    def check_values(self, values):
        for v in values:
            charset, params = v

            assertions.must_be_token(charset)
            assertions.must_be_weight(params)
