# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import helpers
from ..shared import checkers
from ..shared import constraints
from ..shared import cleaners
from ..shared import parameters


def parse_challenges(raw_values):
    """
    Challenge is not cleaned at all.

    :param raw_values:
    :return:
    """
    raw_value = next(raw_values, None)

    if raw_value is None:
        return

    values = []

    try:
        scheme, token_or_param = raw_value.split(' ', 1)
    except ValueError:
        values.append(raw_value)
    else:
        values.extend((scheme, token_or_param))

    for raw_value in raw_values:
        try:
            scheme, token_or_param = raw_value.split(' ', 1)
        except ValueError:
            values.append(raw_value)
        else:
            if checkers.is_token(scheme):
                yield iter(values)
                values = [scheme, token_or_param]
            else:
                values.append(raw_value)

    yield iter(values)


def www_authenticate(
        scheme,
        token=None,
        params=None):
    assert not (token and params)

    return scheme, token, parameters.ParamsCI(params or ())


class WWWAuthenticate(bases.HeaderBase):
    """
    Sent by server only.

    The ``WWW-Authenticate`` header field indicates\
    the authentication scheme(s) and parameters\
    applicable to the target resource.

    Example::

        WWWAuthenticate([
            www_authenticate(
                scheme='Newauth',
                token='asdqwe==')
        ])

        WWWAuthenticate([
            www_authenticate(
                scheme='Newauth',
                params=[('realm', 'apps')]
            )
        ])

        WWWAuthenticate([
            www_authenticate(scheme='Newauth'),
            www_authenticate(scheme='Basic')
        ])

    `Ref. <http://httpwg.org/specs/rfc7235.html#header.www-authenticate>`_
    """

    name = 'www-authenticate'

    def values_str(self, values):
        return ', '.join(
            helpers.format_auth_values(values))

    def prepare_raw_values(self, raw_values_collection):
        return helpers.prepare_multi_raw_values(raw_values_collection)

    def clean_challenge(self, raw_challenge):
        scheme, *token_or_params = raw_challenge

        constraints.must_be_token(scheme)

        scheme = scheme.lower()

        if not token_or_params:
            return scheme, None, parameters.ParamsCI()

        if (len(token_or_params) == 1 and
                checkers.is_token68(token_or_params[0])):
            return scheme, token_or_params[0], parameters.ParamsCI()

        return (scheme,
                None,
                cleaners.clean_params(
                    token_or_params))

    def clean(self, raw_values):
        values = tuple(
            self.clean_challenge(rv)
            for rv in parse_challenges(raw_values))

        constraints.must_not_be_empty(values)

        return values


