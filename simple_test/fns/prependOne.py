# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def prependOne(el):
    def prependOne_inner(collection):
        typedPrependOne = getTypedResult(
            collection, typeToPrependOne, prependOne.__name__
        )
        return typedPrependOne(el, collection)

    return prependOne_inner


# ------- #
# Helpers #
# ------- #


def prependOne_list(el, aList):
    return [el] + aList


typeToPrependOne = {list: prependOne_list}
