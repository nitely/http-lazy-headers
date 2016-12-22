# -*- coding: utf-8 -*-

from ..shared import ascii_tools


# 0-9 / A-Z / a-z
_ALPHA_NUM = frozenset(
    ascii_tools.ascii_chars(
        (0x30, 0x39),
        (0x41, 0x5A),
        (0x61, 0x7A)))

# All visible ASCII chars except delimiters
_TOKEN_CHARS = frozenset('!#$%&\'*+-.^_`|~') | _ALPHA_NUM

# Does not includes "=" sign
_TOKEN68_CHARS = frozenset('-._~+/') | _ALPHA_NUM

# This does not includes "unwise" chars
_URI_CHARS = frozenset('-._~:/?#[]@!$&\'()*+,;=%') | _ALPHA_NUM

# All visible ASCII chars except double quotes
_ETAG_CHARS = frozenset(
    ascii_tools.ascii_chars(0x21, (0x23, 0x7E)))

_MIME_CHARSET_CHARS = frozenset('!#$%&+-^_`{}~') | _ALPHA_NUM
_MIME_CHARSET_VALUE_CHARS = frozenset('!#$%&+-.^_`|~') | _ALPHA_NUM

_LANG_CHARS = frozenset('-') | _ALPHA_NUM

_DIGIT_CHARS = frozenset(
    ascii_tools.ascii_chars((0x30, 0x39)))


def is_token(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_TOKEN_CHARS)


def is_quoted_string(txt):
    """
    This does not validate chars,\
    basically because it allows `quoted-pair`,\
    meaning it allows all valid chars\
    (``HTAB / SP / VCHAR``)

    :param txt:
    :return:
    """
    assert isinstance(txt, str)

    if len(txt) < 2:  # Single quote?
        return False

    if (not txt.startswith('"') and
            not txt.endswith('"')):
        return False

    return True


def is_comment(txt):
    """
    This does not validate chars,\
    basically because it allows `quoted-pair`,\
    meaning it allows all valid chars\
    (``HTAB / SP / VCHAR``)

    :param txt:
    :return:
    """
    assert isinstance(txt, str)

    if (not txt.startswith('(') and
            not txt.endswith(')')):
        return False

    return True


def is_token68(txt):
    """
    http://httpwg.org/specs/rfc7235.html#challenge.and.response
    """
    assert isinstance(txt, str)

    txt = txt.rstrip('=')

    if not txt:
        return False

    return set(txt).issubset(_TOKEN68_CHARS)


def is_uri(txt):
    assert isinstance(txt, str)

    # todo: allow empty?

    return set(txt).issubset(_URI_CHARS)


def is_etag(txt):
    assert isinstance(txt, str)

    if len(txt) < 2:  # Single quote?
        return False

    if (not txt.startswith('"') and
            not txt.endswith('"')):
        return False

    return set(txt[1:-1]).issubset(_ETAG_CHARS)


def is_mime_charset(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_MIME_CHARSET_CHARS)


def is_mime_charset_value(txt):
    assert isinstance(txt, str)

    # May be empty

    return set(txt).issubset(_MIME_CHARSET_VALUE_CHARS)


def is_lang_value(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_LANG_CHARS)


def is_number(txt):
    assert isinstance(txt, str)

    if not txt:
        return False

    return set(txt).issubset(_DIGIT_CHARS)
