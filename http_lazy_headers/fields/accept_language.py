# -*- coding: utf-8 -*-

from ..shared import bases
from ..shared import constraints
from ..shared import quality
from ..shared import helpers
from ..shared import cleaners
from ..shared import parsers
from ..shared import language_tags
from ..shared import parameters


def accept_language(
        lang=None,
        ext_lang=(),
        script=None,
        region=None,
        variant=(),
        extension=(),
        private_use=(),
        grandfathered=None,
        quality=None):
    assert lang or private_use or grandfathered
    assert (
        not private_use or
        (len(private_use) > 1 and
         private_use[0].lower() == 'x'))
    assert all(
        s and ext
        for s, ext in extension)
    assert all(private_use)
    assert all(variant)
    assert all(ext_lang)
    assert len(ext_lang) <= 3
    assert (
        quality is None or
        0 <= quality <= 1)

    params = ()

    if quality is not None:
        params = (('q', quality),)

    return (
        (lang,
         ext_lang,
         script,
         region,
         variant,
         extension,
         private_use,
         grandfathered),
        parameters.Params(params))


class AcceptLanguage(bases.TokensHeaderBase):
    """
    The ``Accept-Language`` header field can\
    be used by user agents to indicate the set\
    of natural languages that are preferred in\
    the response.

    Example::

        AcceptLanguage([
            accept_language('da'),
            accept_language('en', region='gb', quality=0.8),
            accept_language('en', quality=0.7)
            accept_language('*', quality=0.5)
        ])

    `Ref. <http://httpwg.org/specs/rfc7231.html#header.accept-language>`_
    """

    name = 'accept-language'

    def values_str(self, values):
        return ', '.join(
            helpers.format_values_with_params(
                (language_tags.format_language_tag(*value),
                 params)
                for value, params in values))

    def clean_value(self, raw_value):
        raw_value, raw_params = parsers.from_raw_value_with_params(raw_value)

        if raw_value == '*':
            return (
                language_tags.accept_language_value(raw_value),
                cleaners.clean_weight(raw_params))

        return (
            language_tags.clean_language_tag(raw_value),
            cleaners.clean_weight(raw_params))

    def clean(self, raw_values):
        values = tuple(sorted(
            (
                self.clean_value(raw_value)
                for raw_value in raw_values),
            key=quality.quality_sort_key))

        constraints.must_not_be_empty(values)

        return values
