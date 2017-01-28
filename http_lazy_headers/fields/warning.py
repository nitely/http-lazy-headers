# -*- coding: utf-8 -*-

from ..shared.common import hosts
from ..shared.common import dates
from ..shared.generic import cleaners
from ..shared.utils import checkers
from ..shared.utils import constraints
from ..shared.utils import parsers
from ..shared.utils import assertions
from .. import exceptions
from ..shared import bases


def warning(
        code,
        message,
        host=None,
        pseudonym=None,
        date_time=None):
    assert pseudonym or host
    assert not (pseudonym and host)

    return (
        code,
        (host or hosts.host(), pseudonym),
        message,
        date_time)


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
                pseudonym='-',
                message='network down',
                date_time=datetime.now())
        ])

        Warning([
            warning(
                code=112,
                pseudonym='-',
                message='network down')
        ])

    Date-time must match the Date header.

    `Ref. <http://httpwg.org/specs/rfc7234.html#header.warning>`_
    """

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
        code, (host, pseudonym), message, date_time = value

        assertions.must_be_int(code)
        assertions.assertion(
            len(str(code)) == 3,
            '"{}" received, 3 chars int '
            'was expected'.format(code))
        assertions.assertion(
            (pseudonym and
             host == hosts.host()) or
            (not pseudonym and
             host != hosts.host()),
            '"{}" and "{}" received, either '
            'pseudonym or host was expected'
            .format(pseudonym, host))
        pseudonym is None or assertions.must_be_token(pseudonym)
        hosts.check_host(host)
        assertions.must_be_ascii(message)
        (date_time is None or
         assertions.must_be_datetime(date_time))

    def value_str(self, value):
        code, (host, pseudonym), message, date_time = value

        agent = pseudonym or hosts.format_host(host)

        if date_time:
            return (
                '{code} {agent} '
                '{message} "{date_time}"'
                .format(
                    code=code,
                    agent=agent,
                    message=parsers.quote(message),
                    date_time=dates.format_date(date_time)))

        return '{code} {agent} {message}'.format(
            code=code,
            agent=agent,
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
            host = hosts.clean_host(agent)
        except exceptions.HeaderError:
            constraints.must_be_token(agent)
            pseudonym = agent
            host = hosts.host()
        else:
            pseudonym = None

        constraints.must_be_in(code, self.codes_str)
        constraints.constraint(
            checkers.is_quoted_string(text),
            'Text value must be a quoted-string')
        constraints.constraint(
            date is None or
            (len(date) >= 2 and
             date.startswith('"') and
             date.endswith('"')),
            'Date must be a quoted date')

        code = cleaners.clean_number(code, max_chars=3)
        text = parsers.dequote(text)

        if date is not None:
            date = dates.clean_date_time(date[1:-1])

        return code, (host, pseudonym), text, date
