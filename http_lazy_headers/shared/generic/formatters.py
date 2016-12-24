# -*- coding: utf-8 -*-

import urllib.parse

from ..utils import parsers


def format_values_with_params(values, separator=';'):
    for value, params in values:
        if params:
            yield separator.join((
                value,
                str(params)))
        else:
            yield value


def format_auth_values(values):
    for auth_scheme, token, params in values:
        if params:
            params = params.as_str(separator=', ')

        if token and params:
            yield '{} {} {}'.format(
                auth_scheme,
                token,
                params)
        elif token or params:
            yield '{} {}'.format(
                auth_scheme,
                token or params)
        else:
            yield auth_scheme


def format_etag_values(values):
    for etag, is_weak in values:
        if is_weak:
            yield 'W/"{}"'.format(etag)
        else:
            yield '"{}"'.format(etag)


def format_ext_params(params):
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
