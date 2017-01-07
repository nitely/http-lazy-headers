# -*- coding: utf-8 -*-


def vars_for(klass):
    return frozenset((
        getattr(klass, attr)
        for attr in vars(klass)
        if not attr.startswith('_')))
