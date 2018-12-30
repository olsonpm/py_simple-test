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
def mMap(mapperFn):
    fnName = mMap.__name__
    callMapperFn = makeGenericCallFn(mapperFn, 3, fnName)

    def mMap_inner(collection):
        typedMMap = getTypedResult(collection, typeToMMap, fnName)
        return typedMMap(callMapperFn, collection)

    return mMap_inner


# ------- #
# Helpers #
# ------- #


def mMap_list(callMapperFn, aList):
    for idx, el in enumerate(aList):
        aList[idx] = callMapperFn(el, idx, aList)

    return aList


typeToMMap = {list: mMap_list}
