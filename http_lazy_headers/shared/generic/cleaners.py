# -*- coding: utf-8 -*-

import itertools
import urllib.parse

from ..utils import constraints
from ..utils import parsers
from ..utils import checkers
from .. import parameters
from ... import exceptions
from ...settings import settings


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

    # todo: check param_name is a attr-char
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
        not lang or checkers.is_lang_value(lang),
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


def _clean_q_value(raw_q_value):
    """
    Quality q-value

    `Ref. <http://httpwg.org/specs/rfc7231.html#quality.values>`_
    """
    if raw_q_value in {'0', '1'}:
        return int(raw_q_value)

    q_value = clean_float(
        raw_q_value,
        exponent_max_len=1,
        fraction_max_len=3)

    constraints.constraint(
        0 <= q_value <= 1,
        'q value must be equal/greater '
        'than 0 and equal/lesser than 1')

    return q_value


def clean_quality(params):
    """
    Quality parameter

    `Ref. <http://httpwg.org/specs/rfc7231.html#quality.values>`_
    """
    if 'q' not in params:
        return params

    return params.merge({
        'q': _clean_q_value(params['q'])})


def clean_weight(raw_weight):
    """
    Use on headers that only allow\
    quality parameters.

    `Ref. <http://httpwg.org/specs/rfc7231.html#quality.values>`_

    :param raw_weight:
    :return:
    """
    param_name, param_value = clean_param(raw_weight)

    constraints.constraint(
        param_name == 'q',
        'Weight must be in "q=value" format')

    return _clean_q_value(param_value)


def clean_accept_some(raw_value):
    value, raw_weight = parsers.from_raw_value_with_weight(raw_value)

    constraints.must_be_token(value)

    return value.lower(), clean_weight(raw_weight)


def clean_bytes_range(raw_bytes):
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

    (start is None or
     end is None or
     constraints.constraint(
         start <= end,
         'Start must be less/equal than end range'))

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
    not fraction or constraints.must_be_number(fraction)

    try:
        return float(raw_float)
    except ValueError:
        raise exceptions.BadRequest(
            'Value is not a valid float')
