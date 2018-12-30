#
# This file is meant to solve scenarios where flipping the arguments of a
#   utility function presents a readability problem.  My immediate use-case is
#   calling
#
# any(startsWith("full string"))(["possible", "starting", "strings"])
#
# I can't think of a good name for `startsWith` with flipped parameters so a
#   string wrapper which exposes existing utility methods seems good enough,
#   albeit mal-performant.  Also note here we're unable to use
#
# any("full string".startswith)(...)
#
# because the generic utility `any` can't inspect the number of arguments the
#   builtin `startswith` requires.
#

from types import SimpleNamespace as o
from .endsWith import endsWith
from .startsWith import startsWith


def str_(someString):
    def wrap_endsWith(suffix):
        return endsWith(suffix)(someString)

    def wrap_startsWith(prefix):
        return startsWith(prefix)(someString)

    return o(endsWith=wrap_endsWith, startsWith=wrap_startsWith)
