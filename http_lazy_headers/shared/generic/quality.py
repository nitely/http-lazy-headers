# -*- coding: utf-8 -*-


def quality_mime_sort_key(qmt):
    """
    Media ranges can be overridden by more\
    specific media ranges or specific media\
    types. If more than one media range\
    applies to a given type, the most\
    specific reference has precedence.

    Example::

        1. text/plain;format=flowed
        2. text/plain
        3. text/*
        4. */*

    :param qmt:
    :return: Factor as tuple(quality,\
    type_factor, subtype_factor,\
    len_of_params)
    """
    value, params = qmt
    type_, subtype = value

    if type_ != '*':
        type_factor = 1
    else:
        type_factor = 0

    if subtype != '*':
        subtype_factor = 1
    else:
        subtype_factor = 0

    # * -1 otherwise result is reversed
    return (
        params['q'] * -1,
        type_factor * -1,
        subtype_factor * -1,
        len(params) * -1)


def quality_sort_key(qmt):
    """
    Quality of the field.

    :param qmt:
    :return:
    """
    _, params = qmt

    # * -1 otherwise result is reversed
    return params['q'] * -1


def first_of(field_values, values):
    values_map = {
        value: (value, params)
        for value, params in reversed(field_values)
        if params.get('q', 1) > 0}  # Zero q means not acceptable

    for value in values:
        try:
            return values_map[value]
        except KeyError:
            pass
    else:
        raise KeyError


def best_of(field_values, values):
    values = set(values)

    for value, params in field_values:
        if not params.get('q', 1):  # Zero q means not acceptable
            continue

        if value in values:
            return value, params
    else:
        raise KeyError
