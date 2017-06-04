# -*- coding: utf-8 -*-

import datetime

from ..shared.common import entity_tags
from ..shared.common import dates
from ..shared.utils import checkers
from . import etag as etag_field
from ..shared import bases
from ..shared.utils import assertions


def entity_tag(etag):
    return etag_field.entity_tag(
        etag, is_weak=False)


class IfRange(bases.SingleHeaderBase):
    """
    Sent by client only.

    If a client has a partial copy of a\
    representation and wishes to have an\
    up-to-date copy of the entire representation,\
    it could use the Range header field with a\
    conditional GET (using either or both of\
    If-Unmodified-Since and If-Match.) However,\
    if the precondition fails because the\
    representation has been modified, the client\
    would then have to make a second request to\
    obtain the entire current representation.

    The ``If-Range`` header field allows a client\
    to "short-circuit" the second request.\
    Informally, its meaning is as follows: if the\
    representation is unchanged, send me the part(s)\
    that I am requesting in Range; otherwise, send\
    me the entire representation.

    Example::

        IfRange([
            entity_tag('xyzzy')
        ])
        # if-range: "xyzzy"

        IfRange([
            datetime.datetime.now()
        ])

    `Ref. <http://httpwg.org/specs/rfc7233.html#header.if-range>`_
    """

    name = 'if-range'

    def check_one(self, value):
        assertions.must_be_instance_of(
            value, (tuple, datetime.datetime))

        (isinstance(value, datetime.datetime) or
         (entity_tags.check_etag(value)))

        (isinstance(value, datetime.datetime) or
         assertions.assertion(
             not value[1],
             '"{}" received, a strong e-tag '
             'was expected'.format(value)))

    def to_str(self, values):
        value = values[0]

        if isinstance(value, datetime.datetime):
            return dates.format_date(value)
        else:  # e-tag
            return next(entity_tags.format_etags(values))

    def clean_one(self, raw_value):
        # Can't be weak
        if checkers.is_etag(raw_value):
            return raw_value[1:-1], False

        return dates.clean_date_time(
            raw_value, default=datetime.datetime.max)
