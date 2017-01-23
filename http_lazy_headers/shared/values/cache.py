# -*- coding: utf-8 -*-

from ..utils import misc


class CacheDeltaSecsOptions:

    max_age = 'max-age'
    max_stale = 'max-stale'
    min_fresh = 'min-fresh'
    s_maxage = 's-maxage'


class CacheHeadersOptions:

    no_cache = 'no-cache'
    private = 'private'


class CacheOptions(
        CacheDeltaSecsOptions,
        CacheHeadersOptions):
    """"""


CACHE_SECS_VALUES = misc.vars_for(CacheDeltaSecsOptions)
CACHE_HEADERS_VALUES = misc.vars_for(CacheHeadersOptions)
CACHE_VALUES = misc.vars_for(CacheOptions)
