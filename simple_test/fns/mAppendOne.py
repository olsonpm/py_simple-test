# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def mAppendOne(el):
    def mAppendOne_inner(collection):
        typedMAppendOne = getTypedResult(
            collection, typeToMAppendOne, mAppendOne.__name__
        )
        return typedMAppendOne(el, collection)

    return mAppendOne_inner


# ------- #
# Helpers #
# ------- #


def mAppendOne_list(el, aList):
    aList.append(el)
    return aList


typeToMAppendOne = {list: mAppendOne_list}
