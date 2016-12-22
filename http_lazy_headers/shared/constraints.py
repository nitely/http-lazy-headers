# -*- coding: utf-8 -*-

from .. import exceptions
from . import checkers


def constraint(value, explanation='', status=400):
    if not value:
        raise exceptions.HeaderError(
            explanation, status=status)


def must_have_one_value(values):
    constraint(
        len(values) == 1,
        'Header must have one '
        'value and be unique')


def must_not_be_empty(value):
    constraint(
        value,
        'Empty value is not allowed')


def must_be_uri(value):
    constraint(
        checkers.is_uri(value),
        'The URI is not valid')


def must_be_positive(value):
    constraint(
        value >= 0,
        'Value must be greater/equal than 0')


def must_be_token(value):
    constraint(
        checkers.is_token(value),
        'Value must be a token')


def must_be_comment(value):
    constraint(
        checkers.is_comment(value),
        'Value must be a comment')


def must_be_in(value, items):
    constraint(
        value in items,
        '{} is not a valid value'.format(value))


def must_be_etag(value):
    constraint(
        checkers.is_etag(value),
        'Value must be an etag')


def must_be_number(value):
    constraint(
        checkers.is_number(value),
        'Value must be a number')
