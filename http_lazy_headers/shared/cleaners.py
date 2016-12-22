# -*- coding: utf-8 -*-

import itertools
import urllib.parse

from ..settings import settings
from . import checkers
from . import constraints
from . import parameters
from . import parsers
from .. import exceptions


def clean_token(raw_token):
    constraints.must_be_token(raw_token)
    return raw_token


def clean_tokens_ci(raw_tokens):
    return tuple(
        clean_token(rt).lower()
        for rt in parsers.from_tokens(raw_tokens))


def clean_param(raw_param):
    try:
        name, value = raw_param.split('=', 1)
    except ValueError:
        raise exceptions.BadRequest(
            'Expected parameter "name=value" format')

    constraints.must_be_token(name)
    constraints.constraint(
        checkers.is_quoted_string(value) or
        checkers.is_token(value),
        'Param value must be '
        'a token or be quoted')

    if value.startswith('"'):  # Is quoted string
        value = parsers.dequote(value)

    return name, value


def clean_params(raw_params):
    return parameters.ParamsCI(
        clean_param(p)
        for p in raw_params)


def clean_extended_param(raw_param):
    # https://tools.ietf.org/html/rfc5987#section-3.2.1

    param_name, param_value = clean_param(raw_param)

    if not param_name.endswith('*'):
        return param_name, param_value

    # Expects:
    # utf-8'es'%e2%82%ac%20rates
    # or
    # utf-8''%e2%82%ac%20rates

    try:
        charset, lang, value = param_value.split('\'', 2)
    except:
        raise exceptions.BadRequest(
            'Expected "charset\'lang\'value" format')

    constraints.constraint(
        checkers.is_mime_charset(charset),
        'Invalid charset')
    constraints.constraint(
        not lang or checkers.is_lang_value(charset),
        'Invalid language')
    constraints.constraint(
        checkers.is_mime_charset_value(value),
        'Invalid mime value')

    # todo: Support other strategies (ie: ignore param)
    return (
        param_name,
        (
            charset,
            lang or None,
            urllib.parse.unquote(
                value,
                encoding=charset,
                errors='replace')))


def clean_extended_params(raw_params):
    return parameters.ParamsCI(
        clean_extended_param(p)
        for p in raw_params)


def clean_quality(params):
    """
    Quality parameter

    `Ref. <http://httpwg.org/specs/rfc7231.html#quality.values>`_
    """
    if 'q' not in params:
        return params.merge({'q': 1})

    quality_raw = params['q']

    if quality_raw in {'0', '1'}:
        return params.merge({'q': float(quality_raw)})

    quality = clean_float(
        quality_raw,
        exponent_max_len=1,
        fraction_max_len=3)

    constraints.constraint(
        0 <= quality <= 1,
        'q value must be equal/greater '
        'than 0 and equal/lesser than 1')

    return params.merge({'q': quality})


def clean_weight(raw_params):
    """
    Use on headers that only allow\
    quality parameters.

    :param raw_params:
    :return:
    """
    params = parameters.ParamsCI(
        clean_param(p)
        for p in itertools.islice(raw_params, 2))

    constraints.constraint(
        len(params) <= 1,
        'Only weight is allowed')
    constraints.constraint(
        not params or 'q' in params,
        'Weight must be in "q=value" format')

    return clean_quality(params)


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
        clean_params(raw_params))


def clean_accept_some(raw_value):
    value, raw_params = parsers.from_raw_value_with_params(raw_value)

    constraints.must_be_token(value)

    return value.lower(), clean_weight(raw_params)


def clean_etag(raw_value):
    is_weak = False

    if raw_value.startswith('W/'):
        raw_value = raw_value[len('W/'):]
        is_weak = True

    constraints.must_be_etag(raw_value)

    return raw_value[1:-1], is_weak


def clean_bytes_range(raw_bytes):
    # todo: check start >= end

    # Don't allow more/less than one dash
    try:
        start, end = raw_bytes.split('-', 2)
    except ValueError:
        raise exceptions.BadRequest(
            'Param must have start-end format')

    start = start or None
    end = end or None

    if start:
        start = clean_number(
            start, max_chars=settings.CONTENT_MAX_CHARS)

    if end:
        end = clean_number(
            end, max_chars=settings.CONTENT_MAX_CHARS)

    return start, end


def clean_number(raw_number, max_chars=10):
    constraints.constraint(
        len(raw_number) <= max_chars,
        'Number is too big')
    constraints.must_be_number(raw_number)

    try:
        return int(raw_number)
    except ValueError:
        raise exceptions.BadRequest(
            'Value is not a valid number')


def clean_delta_seconds(raw_seconds):
    return clean_number(raw_seconds, max_chars=10)


def clean_float(
        raw_float,
        exponent_max_len=1,
        fraction_max_len=2):
    if len(raw_float) > exponent_max_len + fraction_max_len + 1:  # + dot
        raise exceptions.BadRequest(
            'Value length is too long')

    try:
        exponent, fraction = raw_float.split('.', 1)
    except ValueError:
        raise exceptions.BadRequest(
            'Value must be a float number')

    constraints.constraint(
        len(exponent) <= exponent_max_len,
        'Exponent part contains too many digits')
    constraints.constraint(
        len(fraction) <= fraction_max_len,
        'Fraction part contains too many digits')
    constraints.must_be_number(exponent)
    constraints.must_be_number(fraction)

    try:
        return float(raw_float)
    except ValueError:
        raise exceptions.BadRequest(
            'Value is not a valid float')
