# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def appendAll(collectionToAppend):
    def appendAll_inner(collection):
        typedAppendAll = getTypedResult(
            collection, typeToAppendAll, appendAll.__name__
        )
        return typedAppendAll(collectionToAppend, collection)

    return appendAll_inner


# ------- #
# Helpers #
# ------- #


def appendAll_list(listToAppend, aList):
    return aList + listToAppend


typeToAppendAll = {list: appendAll_list}
