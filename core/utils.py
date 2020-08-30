"""
    Project-wide utility
"""
import logging
import functools
import itertools
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


# ('bytes', 'offset')
XLSX_SIGNATURE = (
    (b'\x50\x4B\x03\x04\x14\x00\x06\x00', 0),   # MS Office Open XML Format Document
    (b'\x50\x4B\x03\x04', 0),                   # MS Office 2007 documents
)
XLS_SIGNATURE = (
    (b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1', 0),   # Microsoft Office document
    # subheaders with offset 512 may be added here too
    # https://www.filesignatures.net/index.php?search=xls&mode=EXT
)

def validate_excel(fobj):
    ''' check xls and xlsx signature
        @return: True, if it valid excel file, False otherwise
    '''
    if not fobj:
        return False

    for sig,offset in itertools.chain(XLSX_SIGNATURE,XLS_SIGNATURE):
        fobj.seek(offset)
        if fobj.tell() != offset:
            continue
        bs = fobj.read(len(sig))
        if bs == sig:
            return True

    return False

