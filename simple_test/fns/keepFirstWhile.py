# ------- #
# Imports #
# ------- #

from .internal.makeGenericCallFn import makeGenericCallFn
from .internal.getTypedResult import getTypedResult
from .decorators.argIsCallable import argIsCallable


# ---- #
# Main #
# ---- #


@argIsCallable
def keepFirstWhile(predicate):
    fnName = keepFirstWhile.__name__
    shouldKeep = makeGenericCallFn(predicate, 3, fnName)

    def keepFirstWhile_inner(collection):
        typedKeepFirstWhile = getTypedResult(
            collection, typeToKeepFirstWhile, fnName
        )
        return typedKeepFirstWhile(shouldKeep, collection)

    return keepFirstWhile_inner


# ------- #
# Helpers #
# ------- #


def keepFirstWhile_list(shouldKeep, aList):
    result = []
    for idx, el in enumerate(aList):
        if not shouldKeep(el, idx, aList):
            break

        result.append(el)

    return result


typeToKeepFirstWhile = {list: keepFirstWhile_list}
