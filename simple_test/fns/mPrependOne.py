# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def mPrependOne(el):
    def mPrependOne_inner(collection):
        typedMPrependOne = getTypedResult(
            collection, typeToMPrependOne, mPrependOne.__name__
        )
        return typedMPrependOne(el, collection)

    return mPrependOne_inner


# ------- #
# Helpers #
# ------- #


def mPrependOne_list(el, aList):
    aList.insert(0, el)
    return aList


typeToMPrependOne = {list: mPrependOne_list}
