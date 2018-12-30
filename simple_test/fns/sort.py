# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def sort(collection):
    typedSort = getTypedResult(collection, typeToSort, "sort")
    return typedSort(collection)


# ------- #
# Helpers #
# ------- #


def sort_dispatched(something):
    return sorted(something)


typeToSort = {list: sort_dispatched}
