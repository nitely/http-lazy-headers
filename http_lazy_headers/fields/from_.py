# -*- coding: utf-8 -*-

from ..shared import bases


def from_(addr, name=None):
    assert isinstance(addr, str)
    assert name is None or isinstance(addr, str)

    # todo: fix
    return addr


class From(bases.SingleHeaderBase):
    """
    Sent by client only.

    The ``From`` header field contains an\
    Internet email address for a human user\
    who controls the requesting user agent.\
    The address ought to be machine-usable.

    Example::

        From(['webmaster@example.org'])

        From(['<webmaster@example.org>'])

        From(['John <webmaster@example.org>'])

        From(['"John Doe" <webmaster@example.org>'])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.from>`_
    """

    # todo: parse the value!

    name = 'from'

    def clean_value(self, raw_value):
        return raw_value
