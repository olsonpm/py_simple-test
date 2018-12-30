# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def append(el):
    def append_inner(collection):
        typedAppend = getTypedResult(collection, typeToAppend, append.__name__)
        return typedAppend(el, collection)

    return append_inner


# ------- #
# Helpers #
# ------- #


def append_list(el, aList):
    result = aList.copy().append(el)
    return result


typeToAppend = {list: append_list}
