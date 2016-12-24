# -*- coding: utf-8 -*-

from . import checkers


def assertion(value, explanation=''):
    if not value:
        raise ValueError(explanation)


def must_be_quality(value):
    if not isinstance(value, (int, float)):
        raise TypeError('Expected int or float type')

    if not 0 <= value <= 1:
        raise ValueError('Quality must be in 0-1 range')


def must_be_token(value):
    assertion(
        checkers.is_token(value),
        'Token was expected, found: {}'.format(value))


def must_be_instance_of(value, klass):
    if isinstance(klass, tuple):
        expected = repr(klass)
    else:
        expected = type(klass)

    assertion(
        isinstance(value, klass),
        '{} was expected, found: {}'.format(
            expected, type(value)))
