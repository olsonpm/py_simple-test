# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def mReverse(collection):
    fnName = mReverse.__name__
    typedMReverse = getTypedResult(collection, typeToMReverse, fnName)
    return typedMReverse(collection)


# ------- #
# Helpers #
# ------- #


def mReverse_dispatched(something):
    something.reverse()
    return something


typeToMReverse = {list: mReverse_dispatched}
