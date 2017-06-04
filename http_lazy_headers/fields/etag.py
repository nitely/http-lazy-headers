# -*- coding: utf-8 -*-

from ..shared.common import entity_tags
from ..shared.generic import formatters
from ..shared.generic import cleaners
from ..shared import bases
from ..shared.utils import assertions
from ..shared.utils import checkers


entity_tag = entity_tags.entity_tag


class ETag(bases.SingleHeaderBase):
    """
    Sent by server only.

    The ``ETag`` header field in a\
    response provides the current\
    entity-tag for the selected\
    representation, as determined at the\
    conclusion of handling the request.\
    An entity-tag is an opaque validator\
    for differentiating between multiple\
    representations of the same resource,\
    regardless of whether those multiple\
    representations are due to resource state\
    changes over time, content negotiation\
    resulting in multiple representations\
    being valid at the same time, or both.\
    An entity-tag consists of an opaque quoted\
    string, possibly prefixed by a weakness
    indicator.

    Example::

        ETag([
            entity_tag('foo123', is_weak=False)
        ])

    `Ref. <http://httpwg.org/specs/rfc7232.html#header.etag>`_
    """
    # todo: match ala http://hyper.rs/hyper/v0.9.12/hyper/header/struct.EntityTag.html

    name = 'etag'

    def check_one(self, value):
        entity_tags.check_etag(value)

    def to_str(self, values):
        return next(entity_tags.format_etags(values))

    def clean_one(self, raw_value):
        return entity_tags.clean_etag(raw_value)
