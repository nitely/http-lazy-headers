# -*- coding: utf-8 -*-

import itertools

from ..utils import constraints
from ..utils import parsers


def prepare_multi_raw_values(raw_values_collection):
    for rvs in raw_values_collection:
        yield from parsers.from_raw_values(rvs)


def prepare_tokens(raw_values_collection):
    for rvs in raw_values_collection:
        yield from parsers.from_tokens(rvs)


def prepare_single_raw_values(raw_values_collection):
    raw_values_collection = tuple(
        itertools.islice(raw_values_collection, 2))
    constraints.must_have_one_value(raw_values_collection)
    return (
        raw_values_collection[0].strip(),)
