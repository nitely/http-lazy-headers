# -*- coding: utf-8 -*-

import datetime

from . import checkers
from .. import parameters
from ... import exceptions


def assertion(value, explanation=''):
    assert isinstance(explanation, str)

    if not value:
        raise exceptions.InternalError(explanation)


def must_be_instance_of(value, klass):
    assertion(
        isinstance(value, klass),
        '"{}" is a {}, {} instance '
        'was expected'.format(
            value,
            type(value),
            repr(klass)))


def must_be_token(value):
    must_be_instance_of(
        value, str)
    assertion(
        checkers.is_token(value),
        '"{}" received, a token '
        'was expected'.format(value))


def must_be_params(params):
    must_be_instance_of(
        params, parameters.Params)

    for p, v in params.items():
        must_be_token(p)
        not isinstance(v, str) or must_be_ascii(v)


def must_be_quality(params):
    must_be_params(params)
    must_be_instance_of(
        params.get('q', 1),
        (int, float))
    assertion(
        0 <= params.get('q', 1) <= 1,
        'Quality must be in 0-1 range')


def must_be_weight(weight):
    (weight is None or
     must_be_instance_of(weight, (int, float)))
    assertion(
        weight is None or
        0 <= weight <= 1,
        '"{}" received, weight in range '
        '0-1 was expected'.format(weight))


def must_be_ascii_params(params):
    must_be_params(params)

    for _, v in params.items():
        must_be_ascii(v)


def must_not_be_empty(value):
    assertion(
        value,
        'Empty value is not allowed')


def must_be_int(value):
    must_be_instance_of(value, int)


def must_have_one_value(values):
    assertion(
        len(values) == 1,
        '"{}" has {} items, 1 item '
        'was expected'.format(
            values, len(values)))


def must_be_ascii(value):
    must_be_instance_of(
        value, str)
    assertion(
        checkers.is_ascii(value),
        '"{}" received, an ascii '
        'was expected'.format(value))


def must_be_ext_token(value):
    must_be_instance_of(
        value, str)
    assertion(
        checkers.is_ext_token(value),
        '"{}" received, a ext-token '
        'was expected'.format(value))


def must_be_encoded_as(value, charset):
    must_be_instance_of(
        value, str)
    must_be_instance_of(
        charset, str)

    try:
        bytes(value, charset)
    except LookupError:
        assertion(
            False,
            '"{}" is not a valid '
            'charset'.format(charset))
    except UnicodeEncodeError:
        assertion(
            False,
            'Can\'t encode "{}" as "{}" '
            'charset'.format(value, charset))


def must_be_uri(value):
    must_be_instance_of(value, str)
    assertion(
        checkers.is_uri(value),
        '"{}" received, URI '
        'was expected'.format(value))


def must_be_visible_chars(value):
    must_be_instance_of(value, str)
    assertion(
        checkers.is_visible_chars(value),
        '"{}" received, 1 or more visible chars '
        'were expected'.format(value))


def must_be_tuple_of(value, length):
    assert isinstance(length, int)

    must_be_instance_of(value, tuple)
    assertion(
        len(value) == length,
        '"{}" received, {} items '
        'were expected'.format(value, length))


def must_be_datetime(value):
    must_be_instance_of(value, datetime.datetime)


def must_be_token68(value):
    must_be_instance_of(value, str)
    assertion(
        checkers.is_token68(value),
        '"{}" received, a token68 '
        'was expected'.format(value))
