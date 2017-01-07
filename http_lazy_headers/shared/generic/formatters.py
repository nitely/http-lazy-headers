# -*- coding: utf-8 -*-

import urllib.parse

from ..utils import parsers


def format_values_with_params(values, separator='; '):
    for value, params in values:
        if params:
            yield separator.join((
                value,
                str(params)))
        else:
            yield value


def format_values_with_weight(values, separator='; '):
    for value, weight in values:
        if weight is None or weight == 1:
            yield value
            continue

        if isinstance(weight, float):
            q = '{:.4}'.format(weight)
        else:
            q = '{}'.format(weight)

        yield separator.join((
            value,
            'q={}'.format(q)))


def format_auth_values(values):
    for auth_scheme, token, params in values:
        if params:
            params = params.as_str(separator=', ')

        #if token and params:
        #    yield '{} {} {}'.format(
        #        auth_scheme,
        #        token,
        #        params)
        if token or params:
            yield '{} {}'.format(
                auth_scheme,
                token or params)
        else:
            yield auth_scheme


def format_ext_params(params):
    # todo: move to common.extended_params.py
    for param_name, param_value in params.items():
        try:
            charset, lang, value = param_value
        except ValueError:
            yield '{}={}'.format(
                param_name,
                parsers.quote_maybe(param_value))
        else:
            yield '{name}={charset}\'{lang}\'{encoded_value}'.format(
                name=param_name,
                charset=charset,
                lang=lang or '',
                encoded_value=urllib.parse.quote(
                    value,
                    safe='',
                    encoding=charset,
                    errors='strict'))
