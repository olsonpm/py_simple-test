# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def prependAll(collectionToPrepend):
    def prependAll_inner(collection):
        typedPrependAll = getTypedResult(
            collection, typeToPrependAll, prependAll.__name__
        )
        return typedPrependAll(collectionToPrepend, collection)

    return prependAll_inner


# ------- #
# Helpers #
# ------- #


def prependAll_list(listToPrepend, aList):
    return aList + listToPrepend


typeToPrependAll = {list: prependAll_list}
