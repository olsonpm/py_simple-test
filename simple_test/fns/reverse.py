# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def reverse(collection):
    fnName = reverse.__name__
    typedReverse = getTypedResult(collection, typeToReverse, fnName)
    return typedReverse(collection)


# ------- #
# Helpers #
# ------- #


def reverse_viaReversed(something):
    return reversed(something)


typeToReverse = {list: reverse_viaReversed}
