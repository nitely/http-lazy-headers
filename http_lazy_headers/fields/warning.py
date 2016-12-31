# -*- coding: utf-8 -*-

from ..shared.common import dates
from ..shared.generic import cleaners
from ..shared.utils import checkers
from ..shared.utils import constraints
from ..shared.utils import parsers
from ..shared.utils import assertions
from .. import exceptions
from ..shared import bases


def warning(code, host_or_token, message, date_time=None, port=None):
    return code, (host_or_token, port), message, date_time


class Warning(bases.MultiHeaderBase):
    """
    Sent by server only.

    The ``Warning`` header field is used to carry\
    additional information about the status or\
    transformation of a message that might not be\
    reflected in the status code. This information\
    is typically used to warn about possible\
    incorrectness introduced by caching operations\
    or transformations applied to the payload\
    of the message.

    Example::

        Warning([
            warning(
                code=112,
                host_or_token='-',
                message='network down',
                date_time=datetime.now())
        ])

        Warning([
            warning(
                code=112,
                host_or_token='-',
                message='network down')
        ])

    Date-time must match the Date header.

    `Ref. <http://httpwg.org/specs/rfc7234.html#header.warning>`_
    """

    # todo: validate host (not uri)

    name = 'warning'
    codes = {
        110,
        111,
        112,
        113,
        199,
        214,
        299}
    codes_str = {
        str(c)
        for c in codes}

    def check_value(self, value):
        assertions.must_be_tuple_of(value, 4)
        assertions.must_be_tuple_of(value[1], 2)

        code, (host_or_token, port), message, date_time = value

        assertions.must_be_int(code)
        assertions.assertion(
            len(str(code)) == 3,
            '"{}" received, 3 chars int '
            'was expected'.format(code))
        assertions.assertion(
            checkers.is_token(host_or_token) or
            checkers.is_uri(host_or_token),
            '"{}" received, token or host '
            'was expected'.format(host_or_token))
        not port or assertions.must_be_int(port)
        assertions.must_be_ascii(message)
        (date_time is None or
         assertions.must_be_datetime(date_time))

    def value_str(self, value):
        code, (host_or_token, port), message, date_time = value

        if port is not None:
            host_or_token = '{}:{}'.format(
                host_or_token, port)

        if date_time:
            return (
                '{code} {token} '
                '{message} "{date_time}"'
                .format(
                    code=code,
                    token=host_or_token,
                    message=parsers.quote(message),
                    date_time=dates.format_date(date_time)))
        else:
            return '{code} {token} {message}'.format(
                code=code,
                token=host_or_token,
                message=parsers.quote(message))

    def values_str(self, values):
        return ', '.join(
            self.value_str(v)
            for v in values)

    def clean_value(self, raw_value):
        raw_values = tuple(parsers.from_raw_values(
            raw_value,
            separator=' '))

        try:
            code, agent, text, date = raw_values
        except ValueError:
            try:
                code, agent, text = raw_values
            except ValueError:
                raise exceptions.BadRequest(
                    'Expected "code agent text date" '
                    'or "code agent text" format')
            else:
                date = None

        try:
            agent, port = agent.split(':', 1)
        except ValueError:
            port = None

        constraints.must_be_in(code, self.codes_str)
        constraints.constraint(
            checkers.is_uri(agent) or
            checkers.is_token(agent),
            'Agent value is not a valid uri or token')
        constraints.constraint(
            checkers.is_quoted_string(text),
            'Text value must be a quoted-string')
        constraints.constraint(
            date is None or
            (len(date) >= 2 and
             date.startswith('"') and
             date.endswith('"')),
            'Date must be a quoted date')

        # May be empty
        if port:
            port = cleaners.clean_number(port, max_chars=5)

        code = cleaners.clean_number(code, max_chars=3)
        text = parsers.dequote(text)

        if date is not None:
            date = dates.clean_date_time(date[1:-1])

        return code, (agent, port), text, date
