# ------- #
# Imports #
# ------- #

from difflib import Differ
from po_simple_test.fns import joinWith, passThrough


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
    result = _d.compare(left.splitlines(keepends=True), right.splitlines(keepends=True))
    return passThrough(result, [list, joinWith("")])
