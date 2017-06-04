# -*- coding: utf-8 -*-

from ..shared.generic import formatters
from ..shared.common import language_tags
from ..shared.generic import cleaners
from ..shared.generic import quality
from ..shared.utils import constraints
from ..shared.utils import parsers
from ..shared import bases
from ..shared import parameters
from ..shared.utils import assertions


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
    return (
        (lang,
         ext_lang,
         script,
         region,
         variant,
         extension,
         private_use,
         grandfathered),
        quality)


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

    def check_one(self, value):
        assertions.must_be_tuple_of(value, 2)

        sub_tags, weight = value

        language_tags.check_language_tag(sub_tags)
        assertions.must_be_weight(weight)

    def to_str(self, values):
        return ', '.join(
            formatters.format_values_with_weight(
                (language_tags.format_language_tag(*value), weight)
                for value, weight in values))

    def clean_one(self, raw_value):
        raw_value, raw_weight = parsers.from_raw_value_with_weight(raw_value)

        if raw_value == '*':
            return (
                language_tags.language_tag(raw_value),
                cleaners.clean_weight(raw_weight))

        return (
            language_tags.clean_language_tag(raw_value),
            cleaners.clean_weight(raw_weight))

    def clean(self, raw_values):
        values = tuple(sorted(
            (
                self.clean_one(raw_value)
                for raw_value in raw_values),
            key=quality.weight_sort_key))

        constraints.must_not_be_empty(values)

        return values
