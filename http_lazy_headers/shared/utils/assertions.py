# -*- coding: utf-8 -*-

from . import checkers
from .. import parameters
from ... import exceptions


def assertion(value, explanation=''):
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


def must_be_params(params):
    must_be_instance_of(
        params, parameters.Params)


def must_be_quality(params):
    must_be_params(params)
    must_be_instance_of(
        params.get('q', 1),
        (int, float))
    assertion(
        0 <= params.get('q', 1) <= 1,
        'Quality must be in 0-1 range')


def must_be_token(value):
    must_be_instance_of(
        value, str)
    assertion(
        checkers.is_token(value),
        '"{}" received, a token '
        'was expected'.format(value))


def must_be_weight(params):
    must_be_quality(params)
    assertion(
        not params or
        (len(params) == 1 and
         'q' in params),
        '"{}" received, weight '
        '<Params([(\'q\', 1)])> was expected'
        .format(params))


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
