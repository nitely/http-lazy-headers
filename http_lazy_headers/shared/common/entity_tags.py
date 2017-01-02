# -*- coding: utf-8 -*-

from ..utils import assertions
from ..utils import checkers
from ..utils import constraints


def entity_tag(etag, is_weak=False):
    assert etag and isinstance(etag, str)

    return etag, is_weak


def check_etag(etag_value):
    assertions.must_be_tuple_of(etag_value, 2)

    etag, is_weak = etag_value

    assertions.must_be_instance_of(etag, str)
    assertions.assertion(
        checkers.is_etag('"{}"'.format(etag)),
        '"{}" received, an etag '
        'was expected'.format(etag))
    assertions.must_be_instance_of(is_weak, bool)


def format_etags(etags):
    for etag, is_weak in etags:
        if is_weak:
            yield 'W/"{}"'.format(etag)
        else:
            yield '"{}"'.format(etag)


def clean_etag(raw_value):
    is_weak = False

    if raw_value.startswith('W/'):
        raw_value = raw_value[len('W/'):]
        is_weak = True

    constraints.must_be_etag(raw_value)

    return raw_value[1:-1], is_weak
