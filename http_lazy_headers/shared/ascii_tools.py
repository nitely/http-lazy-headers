
import itertools


__all__ = [
    'ascii_range',
    'ascii_chars',
    'ascii_range_bytes',
    'ascii_bytes']


def _ascii_range(start, end, to_chr):
    assert isinstance(start, int)
    assert isinstance(end, int)

    return (
        to_chr(cp)
        for cp in range(int(start), int(end) + 1))


def _ascii_chars(*args, to_chr):
    return itertools.chain(*(
        (to_chr(cp),)
        if isinstance(cp, int)
        else _ascii_range(*cp, to_chr=to_chr)
        for cp in args))


def ascii_range(start, end):
    return _ascii_range(start, end, to_chr=chr)


def ascii_chars(*args):
    return _ascii_chars(*args, to_chr=chr)


def _byte(cp):
    return bytes((cp,))


def ascii_range_bytes(start, end):
    return _ascii_range(start, end, to_chr=_byte)


def ascii_bytes(*args):
    return _ascii_chars(*args, to_chr=_byte)
