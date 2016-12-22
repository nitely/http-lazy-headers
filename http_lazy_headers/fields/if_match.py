# -*- coding: utf-8 -*-

from ..shared import bases
from . import etag as etag_field


def match_any():
    return '*', False


def match(etag):
    return etag_field.entity_tag(
        etag, is_weak=False)


class IfMatch(bases.IfMatchSomeBase):
    """
    Sent by client only.

    The ``If-Match`` header field makes the\
    request method conditional on the recipient\
    origin server either having at least one\
    current representation of the target resource,\
    when the field-value is "*", or having a\
    current representation of the target resource\
    that has an entity-tag matching a member of\
    the list of entity-tags provided in the\
    field-value.

    Example::

        IfMatch([
            match('xyzzy')
        ])

        IfMatch([
            match('xyzzy'),
            match('r2d2xxxx'),
            match('c3piozzzz')
        ])

        IfMatch([
            match_any()
        ])
        # if-match: *

    `Ref. <http://httpwg.org/specs/rfc7232.html#header.if-match>`_
    """

    name = 'if-match'
