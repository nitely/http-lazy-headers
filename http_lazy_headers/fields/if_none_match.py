# -*- coding: utf-8 -*-

from ..shared import bases
from . import etag
from . import if_match


entity_tag = etag.entity_tag
match_any = if_match.match_any


class IfNoneMatch(bases.IfMatchSomeBase):
    """
    Sent by client only.

    The ``If-None-Match`` header field makes the\
    request method conditional on a recipient cache\
    or origin server either not having any current\
    representation of the target resource, when the\
    field-value is "*", or having a selected\
    representation with an entity-tag that does not\
    match any of those listed in the field-value.

    Example::

        IfNoneMatch([
            entity_tag('xyzzy')
        ])

        IfNoneMatch([
            entity_tag('xyzzy', is_weak=True)
        ])
        # if-none-match: W/"xyzzy"

        IfNoneMatch([
            entity_tag('xyzzy'),
            entity_tag('r2d2xxxx'),
            entity_tag('c3piozzzz')
        ])

        IfNoneMatch([
            match_any()
        ])
        # if-none-match: *

    `Ref. <http://httpwg.org/specs/rfc7232.html#header.if-none-match>`_
    """

    name = 'if-none-match'
