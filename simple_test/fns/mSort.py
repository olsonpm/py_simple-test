# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def mSort(collection):
    fnName = mSort.__name__
    typedSort = getTypedResult(collection, typeToSort, fnName)
    return typedSort(collection)


# ------- #
# Helpers #
# ------- #


def sort_dispatched(something):
    something.sort()
    return something


typeToSort = {list: sort_dispatched}
