# ------- #
# Imports #
# ------- #

from .internal.getTypedResult import getTypedResult
from .internal.sanitizeAscDesc import sanitizeAscDesc


# ---- #
# Main #
# ---- #


def order(ascOrDesc):
    ascOrDesc = sanitizeAscDesc(ascOrDesc)

    def order_inner(collection):
        fnName = order.__name__
        typedOrder = getTypedResult(collection, typeToOrder, fnName)
        return typedOrder(collection, ascOrDesc)

    return order_inner


# ------- #
# Helpers #
# ------- #


def order_viaSorted(something, ascOrDesc):
    return sorted(something, reverse=(ascOrDesc == "desc"))


typeToOrder = {list: order_viaSorted}
