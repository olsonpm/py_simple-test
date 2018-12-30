# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def discardAll(collectionToDiscard):
    def discardAll_inner(collection):
        typedDiscardAll = getTypedResult(
            collection, typeToDiscardAll, discardAll.__name__
        )
        return typedDiscardAll(collectionToDiscard, collection)

    return discardAll_inner


# ------- #
# Helpers #
# ------- #


def discardAll_list(listToDiscard, aList):
    setToDiscard = set(listToDiscard)
    result = []

    for el in aList:
        if el not in setToDiscard:
            result.append(el)

    return result


typeToDiscardAll = {list: discardAll_list}
