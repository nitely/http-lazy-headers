# -*- coding: utf-8 -*-

from functools import wraps

from .settings import settings


def override_settings(**new_values):
    def decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kw):
            org_values = {
                key: getattr(settings, key)
                for key in new_values}

            for attr, v in new_values.items():
                setattr(settings, attr, v)

            try:
                return func(*args, **kw)
            finally:
                for attr, v in org_values.items():
                    setattr(settings, attr, v)

        return func_wrapper

    return decorator
