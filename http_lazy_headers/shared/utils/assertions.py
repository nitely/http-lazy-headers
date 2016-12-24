# -*- coding: utf-8 -*-

from . import checkers
from .. import parameters


def assertion(value, explanation=''):
    if not value:
        raise ValueError(explanation)


def must_be_instance_of(value, klass):
    assertion(
        isinstance(value, klass),
        '{} instance expected, found: {}'.format(
            repr(klass), type(value)))


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
        'Token was expected, found: {}'.format(value))


def must_be_weight(params):
    must_be_quality(params)
    assertion(
        not params or
        (len(params) == 1 and
         'q' in params),
        'Only weight (q=x) is allowed as a param')
