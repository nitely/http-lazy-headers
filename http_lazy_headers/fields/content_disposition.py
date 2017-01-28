# -*- coding: utf-8 -*-

from ..shared.generic import formatters
from ..shared.generic import cleaners
from ..shared.utils import constraints
from ..shared.utils import parsers
from ..shared import bases
from ..shared import parameters
from ..shared.utils import assertions
from ..shared.utils import checkers


def content_disposition_filename(
        file_name,
        charset='utf-8',
        lang='en',
        disposition_type='attachment',
        fallback_name=None):
    assert (
        file_name and
        isinstance(file_name, str))
    assert (
        not fallback_name or
        isinstance(fallback_name, str))

    fallback_name = str(
            bytes(
                fallback_name or file_name,
                encoding='ascii',
                errors='replace'),
            encoding='ascii')

    return (
        disposition_type,
        parameters.Params((
            ('filename', fallback_name),
            ('filename*', (charset, lang, file_name)),)))


class ContentDisposition(bases.SingleHeaderBase):
    """
    Sent by server only.

    Is up to the user to recover from a bad file name or not.

    This is the only header supporting ISO-8859-1\
    on quoted-string param value, however appendix-D\
    says to use us-ascii on filename.

    The ``Content-Disposition`` response header field is\
    used to convey additional information about how to\
    process the response payload, and also can be used\
    to attach additional metadata, such as the filename\
    to use when saving the response payload locally.

    Example::

        ContentDisposition([
            content_disposition_filename('áéíóú.zip')
        ])

        ContentDisposition([(
            Disposition.attachment,
            Params([
                ('filename*', ('utf-8', 'en', 'áéíóú.zip'))
            ])
        )])

        ContentDisposition([(
            Disposition.attachment,
            Params([
                ('filename*', ('utf-8', None, 'áéíóú.zip'))
            ])
        )])

        ContentDisposition([(
            Disposition.attachment,
            Params([
                ('filename', 'aeiou.zip'),
                ('filename*', ('utf-8', None, 'áéíóú.zip'))
            ])
        )])

    `Ref. <https://tools.ietf.org/html/rfc6266>`_
    """

    name = 'content-disposition'

    def check_value(self, value):
        assertions.must_be_tuple_of(value, 2)
        disposition_type, params = value
        assertions.must_be_token(disposition_type)
        assertions.must_be_params(params)

        for p, v in params.items():
            assertions.must_be_instance_of(v, (str, tuple))

            if isinstance(v, str):
                assertions.assertion(
                    not p.endswith('*'),
                    '"{}" has extended format name '
                    '(ends with "*"), a tuple '
                    'was expected'.format(p))
                assertions.must_be_ext_token(p)
                assertions.must_be_ascii(v)
                continue

            assertions.assertion(
                p.endswith('*'),
                '"{}" is a extended param, '
                'a "*" at the end of the '
                'name was expected'.format(p))
            assertions.must_be_ext_token(p[:-1])
            assertions.assertion(
                len(v) == 3,
                '"{}" has {} items, 3 items '
                'were expected'.format(v, len(v)))

            assertions.must_be_tuple_of(v, 3)
            charset, lang, mime_value = v
            assertions.must_be_instance_of(charset, str)
            assertions.assertion(
                checkers.is_mime_charset(charset),
                '"{}" is not a valid charset'
                .format(charset))
            not lang or assertions.must_be_instance_of(lang, str)
            not lang or assertions.assertion(
                checkers.is_lang_value(lang),
                '"{}" is not a valid language'
                .format(lang))
            assertions.must_be_encoded_as(mime_value, charset)

    def values_str(self, values):
        disposition_type, params = values[0]

        return '; '.join((
            disposition_type,
            *formatters.format_ext_params(params)))

    def clean_value(self, raw_value):
        # See test cases: http://greenbytes.de/tech/tc2231/#c-d-inline
        raw_value, raw_params = parsers.from_raw_value_with_params(raw_value)
        constraints.must_be_token(raw_value)

        value = raw_value.lower()
        params = cleaners.clean_extended_params(raw_params)

        # Don't allow file-names with absolute path
        constraints.constraint(
            not params
            .get('filename', '')
            .startswith(('/', '\\')) and
            not params
            .get('filename*', (None, None, ''))[2]
            .startswith(('/', '\\')),
            'Filename can\'t be absolute')

        return value, params
