# -*- coding: utf-8 -*-

from ..settings import settings
from ..shared import bases
from ..shared import cleaners
from ..shared import constraints
from ..shared import helpers


class ContentLength(bases.HeaderBase):
    """
    When a message does not have a\
    ``Transfer-Encoding`` header field,\
    a ``Content-Length`` header field can\
    provide the anticipated size, as a decimal\
    number of octets, for a potential payload\
    body. For messages that do include a payload\
    body, the Content-Length field-value provides\
    the framing information necessary for\
    determining where the body (and message) ends.\
    For messages that do not include a payload body,\
    the Content-Length indicates the size of the\
    selected representation.

    Example::

        ContentLength([3495])

    `Ref. <http://httpwg.org/specs/rfc7230.html#header.content-length>`_
    """

    name = 'content-length'

    def values_str(self, values):
        return str(values[0])

    def prepare_raw_values(self, raw_values_collection):
        return helpers.prepare_multi_raw_values(raw_values_collection)

    def clean(self, raw_values):
        raw_values = set(raw_values)
        constraints.must_have_one_value(raw_values)
        return (
            cleaners.clean_number(
                tuple(raw_values)[0],
                max_chars=max(10, settings.CONTENT_MAX_SIZE)),)
