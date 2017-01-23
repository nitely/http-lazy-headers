# -*- coding: utf-8 -*-

from ..utils import constraints
from ..utils import checkers
from ..utils import assertions
from ..utils import ascii_tools
from ... import exceptions


# A-Z / a-z
_ALPHA = frozenset(
    ascii_tools.ascii_chars(
        (0x41, 0x5A),
        (0x61, 0x7A)))


(LANG,
 EXT_LANG,
 SCRIPT,
 REGION,
 VARIANT,
 EXTENSION,
 PRIVATE_USE,
 GRANDFATHERED) = range(8)

_GRANDFATHERED_MAP = {
    # Irregular
    'en-gb-oed': 'en-gb-oxendict',
    'i-ami': 'ami',
    'i-bnn': 'bnn',
    'i-default': None,
    'i-enochian': None,
    'i-hak': 'hak',
    'i-klingon': 'tlh',
    'i-lux': 'lb',
    'i-mingo': None,
    'i-navajo': 'nv',
    'i-pwn': 'pwn',
    'i-tao': 'tao',
    'i-tay': 'tay',
    'i-tsu': 'tsu',
    'sgn-be-fr': 'sfb',
    'sgn-be-nl': 'vgt',
    'sgn-ch-de': 'sgg',

    # Regular
    'art-lojban': 'jbo',
    'cel-gaulish': None,
    'no-bok': 'nb',
    'no-nyn': 'nn',
    'zh-guoyu': 'cmn',
    'zh-hakka': 'hak',
    'zh-min': None,
    'zh-min-nan': 'nan',
    'zh-xiang': 'hsn'}


def is_alpha(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_ALPHA)


def is_sub_tag(txt):
    assert isinstance(txt, str)

    return len(txt) <= 8 and checkers.is_alphanum(txt)


def check_language_tag(value):
    assertions.must_be_tuple_of(value, 8)

    (lang,
     ext_lang,
     script,
     region,
     variant,
     extension,
     private_use,
     grandfathered) = value

    assertions.assertion(
        lang or private_use or grandfathered,
        '"{}" received, lang, private-use or '
        'grandfathered was expected'.format(value))
    assertions.assertion(
        not (grandfathered and
             any(st
                 for st in value[:-1])),
        '"{}" received, all empty but '
        'grandfathered or the inverse '
        'was expected'.format(value))

    (lang is None or
     assertions.must_be_instance_of(lang, str))
    (lang is None or
     assertions.assertion(
         2 <= len(lang) <= 8 and
         is_alpha(lang),
         'Lang must have 8 or less chars'))

    assertions.assertion(
        isinstance(ext_lang, tuple) and
        len(ext_lang) <= 3,
        '"{}" received, ext-lang tuple '
        'of 3 or less was expected'
        .format(ext_lang))
    assertions.assertion(
        all(isinstance(st, str) and
            len(st) <= 8 and
            is_alpha(st)
            for st in ext_lang),
        '"{}" received, ext-lang of str '
        'and less/equal than 8 alpha '
        'chars was expected'.format(lang))

    (script is None or
     assertions.must_be_instance_of(script, str))
    (script is None or
     assertions.assertion(
         len(script) == 4 and
         is_alpha(script),
         '"{}" received, script of '
         'less/equal than 4 alpha '
         'chars was expected'.format(script)))

    (region is None or
     assertions.must_be_instance_of(region, str))
    (region is None or
     assertions.assertion(
         (len(region) == 2 and
          is_alpha(region)) or
         (len(region) == 3 and
          checkers.is_number(region)),
         '"{}" received, either a region of '
         '2 alpha chars or 3 numbers '
         'was expected'.format(region)))

    assertions.must_be_instance_of(variant, tuple)
    assertions.assertion(
        all((isinstance(st, str) and
             checkers.is_alphanum(st)) and
            (5 <= len(st) <= 8 or
             (len(st) == 4 and
              checkers.is_number(st[0])))
            for st in variant),
        '"{}" received, either a variant of '
        '5-8 alphanum chars or 4 alphanum chars '
        '(with the first char as number) '
        'was expected'.format(variant))

    assertions.must_be_instance_of(extension, tuple)

    for ext in extension:
        assertions.must_be_tuple_of(ext, 2)

        st, sts = ext

        assertions.assertion(
            isinstance(st, str) and
            len(st) == 1 and
            checkers.is_alphanum(st),
            '"{}" received, extension key of '
            '1 alphanum was expected'.format(st))

        assertions.assertion(
            isinstance(sts, str) and
            2 <= len(sts) <= 8 and
            checkers.is_alphanum(sts),
            '"{}" received, extension value of '
            '2-8 alphanum chars was expected'
            .format(sts))

    assertions.assertion(
        len(extension) == len(set(
            dict(extension).keys())),
        '"{}" received, unique extension '
        'keys was expected'.format(extension))

    assertions.must_be_instance_of(private_use, tuple)
    not private_use or assertions.assertion(
        len(private_use) > 1 and
        isinstance(private_use[0], str) and
        private_use[0].lower() == 'x',
        '"{}" received, an "x" as first '
        'value was expected'.format(private_use))
    assertions.assertion(
        all(isinstance(st, str) and
            st <= 8 and
            checkers.is_alphanum(st)
            for st in private_use),
        '"{}" received, tags of alphanum chars'
        'less/equal than 8 was expected'
        .format(private_use))

    (grandfathered is None or
     assertions.must_be_instance_of(grandfathered, str))
    (grandfathered is None or
     assertions.assertion(
         grandfathered.lower() in _GRANDFATHERED_MAP,
         '"{}" received, grandfathered '
         'in "{}" was expected'.format(
             grandfathered,
             _GRANDFATHERED_MAP)))


def format_language_tag(
        lang,
        ext_lang,
        script,
        region,
        variant,
        extension,
        private_use,
        grandfathered):
    if grandfathered:
        return grandfathered

    # Extensions must be ordered,
    # see https://tools.ietf.org/html/rfc5646#section-4.5
    extension = (
        '{}-{}'.format(key, '-'.join(ext))
        for key, ext in sorted(extension))

    return '-'.join(
        sub_tag
        for sub_tag in (
            lang,
            '-'.join(ext_lang),
            script,
            region,
            '-'.join(variant),
            '-'.join(extension),
            '-'.join(private_use))
        if sub_tag)


def language_tag(
        lang=None,
        ext_lang=(),
        script=None,
        region=None,
        variant=(),
        extension=(),
        private_use=(),
        grandfathered=None):
    assert any(locals().values())

    return (
        lang,
        ext_lang,
        script,
        region,
        variant,
        extension,
        private_use,
        grandfathered)


def _preferred_language_tag(raw_language_tag):
    return (_GRANDFATHERED_MAP.get(raw_language_tag, None) or
            raw_language_tag)


def clean_language_tag(raw_language_tag):
    # https://tools.ietf.org/html/rfc5646#section-2.1

    raw_language_tag = _preferred_language_tag(
        raw_language_tag.lower())

    if raw_language_tag in _GRANDFATHERED_MAP:
        return language_tag(
            grandfathered=raw_language_tag)

    curr = LANG
    lang_tag = [None for _ in range(8)]
    ext_lang = []
    variants = []
    extensions = []
    seen_extensions = set()
    privates = []

    for sub_tag in raw_language_tag.split('-', 50):
        constraints.constraint(
            is_sub_tag(sub_tag),
            'A valid sub-tag was expected')

        sub_tag_len = len(sub_tag)

        if curr == LANG:
            constraints.constraint(
                sub_tag_len >= 2)
            constraints.constraint(
                is_alpha(sub_tag))

            lang_tag[LANG] = sub_tag

            if sub_tag_len < 4:
                curr = EXT_LANG
            else:
                curr = SCRIPT

            continue

        if curr == EXT_LANG:
            if (sub_tag_len == 3 and
                    len(ext_lang) < 3 and
                    is_alpha(sub_tag)):
                ext_lang.append(sub_tag)
                continue

            curr = SCRIPT

        if curr == SCRIPT:
            curr = REGION

            if sub_tag_len == 4 and is_alpha(sub_tag):
                lang_tag[SCRIPT] = sub_tag
                continue

        if curr == REGION:
            curr = VARIANT

            if sub_tag_len == 2 and is_alpha(sub_tag):
                lang_tag[REGION] = sub_tag
                continue

            if sub_tag_len == 3 and checkers.is_number(sub_tag):
                lang_tag[REGION] = sub_tag
                continue

        if curr == VARIANT:
            if sub_tag_len >= 5:
                variants.append(sub_tag)
                continue

            if sub_tag_len == 4 and checkers.is_number(sub_tag[0]):
                variants.append(sub_tag)
                continue

            curr = EXTENSION

        # https://tools.ietf.org/html/rfc5646#section-2.2.6
        if curr == EXTENSION:
            if sub_tag_len == 1 and sub_tag[0] != 'x':
                constraints.constraint(
                    sub_tag not in seen_extensions,
                    'Extension must not be duplicated')

                extensions.append((sub_tag, []))
                seen_extensions.add(sub_tag)
                continue

            if sub_tag_len >= 2 and extensions:
                extensions[-1][1].append(sub_tag)
                continue

            curr = PRIVATE_USE

        if curr == PRIVATE_USE:
            if sub_tag_len == 1 and sub_tag[0] == 'x':
                privates.append(sub_tag)
                continue

            if privates:
                privates.append(sub_tag)
                continue

        raise exceptions.HeaderError('Bad language-tag')

    constraints.constraint(
        lang_tag[LANG] or privates,
        'Value must have a language, '
        'private-use or grandfathered')
    constraints.constraint(
        all(
            ext[1]
            for ext in extensions),
        'Extension must have a value')
    constraints.constraint(
        not privates or len(privates) > 1,
        'Private-use must have a value')

    lang_tag[EXT_LANG] = tuple(ext_lang)
    lang_tag[VARIANT] = tuple(variants)
    lang_tag[EXTENSION] = tuple(
        (ext[0], tuple(ext[1]))
        for ext in extensions)
    lang_tag[PRIVATE_USE] = tuple(privates)

    return language_tag(*lang_tag)
