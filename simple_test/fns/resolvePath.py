#
# README
#  - a re-implementation of node's `path.resolve`
#

from os import path
from os.path import abspath, isabs, normpath
from .decorators.argIsListOfType import argIsListOfType
from .isEmpty import isEmpty
from .passThrough import passThrough


def joinPaths(segments):
    return path.join(*segments)


@argIsListOfType(str)
def resolvePath(segments):
    if isEmpty(segments):
        return ""

    relevantSegments = []
    for aSegment in reversed(segments):
        relevantSegments.append(aSegment)

        if isabs(aSegment):
            break

    relevantSegments.reverse()

    return passThrough(relevantSegments, [joinPaths, normpath, abspath])
