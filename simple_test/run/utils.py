# ------- #
# Imports #
# ------- #

from glob import glob
from os import path
from ..fns import forEach, resolvePath
from ..suite import suite
from ..test import test
import importlib.util


# ---- #
# Main #
# ---- #


#
# I'm choosing to gather all the tests prior to running any because I feel that
#   will be a simpler design.
#
def gatherTests(aSuite):
    oldCurrentSuite = aSuite.rootState.currentSuite
    aSuite.rootState.currentSuite = aSuite
    aSuite.fn()
    forEach(gatherTests)(aSuite.suites)
    aSuite.rootState.currentSuite = oldCurrentSuite


def importFilesInDir(aDir, idx):
    for innerIdx, aFile in enumerate(glob(resolvePath([aDir, "*.py"]))):
        importFile(aFile, idx, "_" + str(innerIdx))


def importFile(aFile, idx, innerIdx=""):
    # TODO: find out if this name has to be unique - might be unnecessary
    spec = importlib.util.spec_from_file_location(
        f"test{idx}{innerIdx}_{path.basename(aFile)}", aFile
    )
    testModule = importlib.util.module_from_spec(spec)
    testModule.test = test
    testModule.suite = suite
    spec.loader.exec_module(testModule)


def toResolvedPath(fromAbsDir):
    def toResolvedPath_inner(aPath):
        return resolvePath([fromAbsDir, aPath])

    return toResolvedPath_inner


def recursiveGlob(globStr):
    return glob(globStr, recursive=True)
