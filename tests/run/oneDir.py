# ------- #
# Imports #
# ------- #

from types import SimpleNamespace as o
from simple_test import run
from simple_test.fns import noop
from .utils import makeGetPathToFixture


# ---- #
# Init #
# ---- #

getPathToFixture = makeGetPathToFixture("oneDir")

success = getPathToFixture("success")
fail = getPathToFixture("fail")
noTests = getPathToFixture("noTests")
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
        r.addError(code)

    #
    # with rootDir and globStr
    #
    code = "run(globStr='*.py', rootDir=success, report=spyReport)"
    spyReportResult = o(wasCalled=False)
    result = run(globStr="*.py", rootDir=success, report=spyReport)
    passed = (
        result.succeeded
        and result.testsFound
        and len(result.rootTests) == 1
        and spyReportResult.wasCalled
        and spyReportResult.state is result
    )
    if not passed:
        print(result.testsFound)
        r.addError(code)

    code = "run(filesAndDirs=[fail])"
    try:
        result = run(filesAndDirs=[fail])
        r.shouldHaveRaisedAnError(code)
    except:
        pass

    code = "run(filesAndDirs=[noTests], report=noop)"
    result = run(filesAndDirs=[noTests], report=noop)
    passed = result.succeeded and not result.testsFound
    if not passed:
        r.addError(code)

    return r
