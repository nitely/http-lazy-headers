# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import cleaners
from ..shared import helpers


def entity_tag(etag, is_weak=False):
    assert etag and isinstance(etag, str)

    return etag, is_weak


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

    def values_str(self, values):
        return next(helpers.format_etag_values(values))

    def clean_value(self, raw_value):
        return cleaners.clean_etag(raw_value)
