from types import SimpleNamespace as o
from copy import copy

#
# assigns attributes of primaryObj over secondaryObj
# this is intended to consume instances of SimpleNamespace, but not restricted
#   to such
# returns an instance of SimpleNamespace
#


def assign(primaryObj):
    simplePrimary = o()
    for k, v in primaryObj.__dict__.items():
        setattr(simplePrimary, k, v)

    def assign_inner(secondaryObj):
        result = copy(simplePrimary)

        for k, v in secondaryObj.__dict__.items():
            if k not in result.__dict__:
                setattr(result, k, v)

        return result

    return assign_inner
