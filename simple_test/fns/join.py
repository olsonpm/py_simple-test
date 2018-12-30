# ------- #
# Imports #
# ------- #

from ordered_set import OrderedSet
from .internal.getTypedResult import getTypedResult


# ---- #
# Main #
# ---- #


def join(separator):
    def join_inner(collection):
        typedJoin = getTypedResult(collection, typeToJoin, "join")
        return typedJoin(separator, collection)

    return join_inner


# ------- #
# Helpers #
# ------- #


def join_iterable(separator, aList):
    return separator.join(aList)


typeToJoin = {list: join_iterable, OrderedSet: join_iterable}
