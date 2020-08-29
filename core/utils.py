"""
    Project-wide utility
"""
import logging
import functools
from copy import deepcopy

from core import consts


class dotdict(dict):
    """ dot.notation access to dictionary attributes
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class EnumSearch():
    @classmethod
    def search(cls, term):
        for member in cls:
            if member.label.lower() == term.lower():
                return member
        return None


def lru_cache(maxsize=128, typed=False, copy=False):
    """ set copy=True, if you need safely mutable results
    """

    if not copy:
        return functools.lru_cache(maxsize, typed)
    def decorator(f):
        cached_func = functools.lru_cache(maxsize, typed)(f)
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return deepcopy(cached_func(*args, **kwargs))
        return wrapper
    return decorator


