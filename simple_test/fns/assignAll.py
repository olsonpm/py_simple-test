#
# README
#  - Similar to javascript's Object.assign, this assigns attributes right to
#    left, meaning objects to the right take precedence to those on the left
#
#  takes a list of SimpleNamespace instances
#  returns an instance of SimpleNamespace
#

from types import SimpleNamespace as o
from .discardWhen import discardWhen
from .isInstanceOf import isInstanceOf
from .isLaden import isLaden
from .raise_ import raise_


def assignAll(aList):
    validateInput(aList)
    result = o()

    for obj in aList:
        for key, val in obj.__dict__.items():
            result[key] = val

    return result


# ------- #
# Helpers #
# ------- #


def validateInput(aList):
    if not isinstance(aList, list):
        raise_(
            ValueError,
            f"""
            aList must be an instance of list
            type given: {type(aList).__name__}
            """,
        )

    invalidElements = discardWhen(isInstanceOf(o))(aList)
    if isLaden(invalidElements):
        n = len(invalidElements)
        raise_(
            ValueError,
            f"""
            aList contains {n} elements which aren't an instance
            of SimpleNamespace

            first invalid element: {str(invalidElements[0])}
            """,
        )
