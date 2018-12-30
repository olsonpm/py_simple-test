# ------- #
# Imports #
# ------- #

from difflib import Differ
from simple_test.fns import join, passThrough


# ---- #
# Init #
# ---- #

_d = Differ()


# ---- #
# Main #
# ---- #


def getModuleBasename(m):
    return m.__name__.split(".")[-1]


def diff(left, right):
    result = _d.compare(
        left.splitlines(keepends=True), right.splitlines(keepends=True)
    )
    return passThrough(result, [list, join("")])
