# ------- #
# Imports #
# ------- #

from types import SimpleNamespace as o
from simple_test import run
from simple_test.fns import noop
from .utils import makeGetPathToFixture
import os


# ---- #
# Init #
# ---- #

getPathToFixture = makeGetPathToFixture("oneFile")

success = getPathToFixture("success.py")
successDir = os.path.dirname(success)
fail = getPathToFixture("fail.py")
noTests = getPathToFixture("noTests.py")
spyReportResult = None


def spyReport(state):
    global spyReportResult
    spyReportResult = o(wasCalled=True, state=state)


# ---- #
# Main #
# ---- #


def runTests(r):
    global spyReportResult

    code = "run(filesAndDirs=[success], report=spyReport)"
    spyReportResult = o(wasCalled=False)
    result = run(filesAndDirs=[success], report=spyReport)
    passed = (
        result.succeeded
        and result.testsFound
        and len(result.rootTests) == 1
        and spyReportResult.wasCalled
        and spyReportResult.state is result
    )
    if not passed:
        print(spyReportResult.state is result)
        r.addError(code)

    #
    # silent
    #
    code = "run(filesAndDirs=[success], silent=True, report=spyReport)"
    spyReportResult = o(wasCalled=False)
    result = run(filesAndDirs=[success], silent=True, report=spyReport)
    passed = (
        result.succeeded
        and result.testsFound
        and len(result.rootTests) == 1
        and not spyReportResult.wasCalled
    )
    if not passed:
        r.addError(code)

    #
    # with rootDir
    #
    code = (
        "run(filesAndDirs=['success.py'], rootDir=successDir"
        ", report=spyReport)"
    )
    spyReportResult = o(wasCalled=False)
    result = run(
        filesAndDirs=["success.py"], rootDir=successDir, report=spyReport
    )
    passed = (
        result.succeeded
        and result.testsFound
        and len(result.rootTests) == 1
        and spyReportResult.wasCalled
    )
    if not passed:
        r.addError(code)

    try:
        code = "run(filesAndDirs=[fail])"
        run(filesAndDirs=[fail])
        r.shouldHaveRaisedAnError(code)
    except:
        pass

    code = "run(filesAndDirs=[noTests], report=noop)"
    result = run(filesAndDirs=[noTests], report=noop)
    passed = result.succeeded and not result.testsFound
    if not passed:
        r.addError(code)

    return r
