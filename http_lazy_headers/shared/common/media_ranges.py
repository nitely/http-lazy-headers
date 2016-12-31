# -*- coding: utf-8 -*-

from ..utils import constraints
from ..utils import parsers
from ..generic import cleaners
from ..generic import formatters
from ..utils import assertions
from ... import exceptions


def check_value(value):
    assertions.must_be_tuple_of(value, 2)
    assertions.must_be_tuple_of(value[0], 2)

    (top_level, sub_level), params = value

    assertions.must_be_token(top_level)
    assertions.must_be_token(sub_level)
    assertions.must_be_params(params)


def format_media_ranges(values):
    return formatters.format_values_with_params(
        ('/'.join(mime), params)
        for mime, params in values)


def clean_media_type(raw_value):
    """
    MediaType item. For Content-Type and Accept headers.

    The type, subtype, and parameter name are case-insensitive.\
    Parameter values might be case-sensitive,\
    depending on the semantics of the parameter name.

    text/html;foo=bar;bar="foo\;bar"

    `Ref. <http://httpwg.org/specs/rfc7231.html#media.type>`_
    """
    raw_value, raw_params = parsers.from_raw_value_with_params(raw_value)

    try:
        type_, subtype = raw_value.split('/', 1)
    except ValueError:
        raise exceptions.BadRequest(
            'Expected "type/subtype" format')

    constraints.must_be_token(type_)
    constraints.must_be_token(subtype)

    return (
        (type_, subtype),
        cleaners.clean_params(raw_params))
