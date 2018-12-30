from textwrap import dedent
from types import SimpleNamespace as o
from copy import copy

#
# combines the attributes of obj1 and obj2 while ensuring none are overwritten
# this is intended to consume instances of SimpleNamespace, but not restricted
#   to such
# returns an instance of SimpleNamespace
#


def combine(primaryObj):
    simplePrimary = o()
    for k, v in primaryObj.__dict__.items():
        setattr(simplePrimary, k, v)

    def combine_inner(secondaryObj):
        result = copy(simplePrimary)

        for k, v in secondaryObj.__dict__.items():
            if k in result.__dict__:
                _raiseOverlappingKeysError(k)
            else:
                setattr(result, k, v)

        return result

    return combine_inner


def _raiseOverlappingKeysError(key):
    raise ValueError(
        dedent(
            f"""
            'combine' was passed two objects with matching attribute keys
            key: {key}
            """
        )
    )
