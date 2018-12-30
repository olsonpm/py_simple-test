# ------- #
# Imports #
# ------- #

from os import path
from simple_test_default_reporter import report as defaultReport
from .runAllTests import runAllTests
from .validateRunParams import validateRunParams
from ..state import initState
import os

from .utils import (
    gatherTests,
    importFile,
    importFilesInDir,
    recursiveGlob,
    toResolvedPath,
)

from ..fns import forEach, isSomething, map_, passThrough


# ---- #
# Main #
# ---- #


def run(
    *, filesAndDirs=None, globStr=None, report=None, rootDir=None, silent=False
):
    state = initState()
    validateRunParams(filesAndDirs, globStr, report, rootDir, silent)

    if report is None and not silent:
        report = defaultReport

    if rootDir is None:
        rootDir = os.getcwd()
    else:
        rootDir = path.abspath(rootDir)

    if isSomething(globStr):
        filesAndDirs = passThrough(
            globStr,
            [toResolvedPath(rootDir), recursiveGlob, map_(path.normpath)],
        )
    else:
        filesAndDirs = map_(toResolvedPath(rootDir))(filesAndDirs)

    for idx, fileOrDir in enumerate(filesAndDirs):
        if os.path.isdir(fileOrDir):
            importFilesInDir(fileOrDir, idx)
        else:
            importFile(fileOrDir, idx)

    forEach(gatherTests)(state.rootSuites)
    runAllTests(state)

    if not silent:
        report(state)

    return state
