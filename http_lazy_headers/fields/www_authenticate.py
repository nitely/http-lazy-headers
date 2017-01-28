# -*- coding: utf-8 -*-

from ..shared.generic import formatters
from ..shared.generic import cleaners
from ..shared.generic import preparers
from ..shared.utils import checkers
from ..shared.utils import constraints
from ..shared.utils import assertions
from ..shared import bases
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

    def check_values(self, values):
        assertions.must_not_be_empty(values)

        for v in values:
            assertions.must_be_tuple_of(v, 3)
            scheme, token, params = v
            assertions.must_be_token(scheme)
            token is None or assertions.must_be_token68(token)
            assertions.must_be_ascii_params(params)
            assertions.assertion(
                not (token and params),
                '"{}" and "{}" received, either '
                'token or params was expected'
                .format(token, params))

    def values_str(self, values):
        return ', '.join(
            formatters.format_auth_values(values))

    def prepare_raw_values(self, raw_values_collection):
        return preparers.prepare_multi_raw_values(raw_values_collection)

    def clean_challenge(self, raw_challenge):
        scheme, *token_or_params = raw_challenge
        constraints.must_be_token(scheme)
        scheme = scheme.lower()

        if not token_or_params:
            return (
                scheme,
                None,
                parameters.ParamsCI())

        if (len(token_or_params) == 1 and
                checkers.is_token68(token_or_params[0])):
            return (
                scheme,
                token_or_params[0],
                parameters.ParamsCI())

        return (
            scheme,
            None,
            cleaners.clean_params(
                token_or_params))

    def clean(self, raw_values):
        values = tuple(
            self.clean_challenge(rv)
            for rv in parse_challenges(raw_values))

        constraints.must_not_be_empty(values)

        return values


