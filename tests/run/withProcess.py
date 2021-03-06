# ------- #
# Imports #
# ------- #

from os import path
from po_simple_test.fns import justReturn
from po_simple_test.run import createRun
from types import SimpleNamespace as o
import sys


# ---- #
# Init #
# ---- #


def spySubprocessRun(*args, **kwargs):
    global spyResult
    spyResult = o(args=args, kwargs=kwargs)
    return o(returncode=0, stdout="success")


currentDir = path.dirname(path.abspath(__file__))
projectDir = path.join(currentDir, "fixtures", "project")
spyResult = None
spyRun = createRun(spySubprocessRun)
successRun = createRun(justReturn(o(returncode=0)))
failRun = createRun(justReturn(o(returncode=1)))
errorRun = createRun(justReturn(o(returncode=2)))


def runTests(r):
    code = "successRun(projectDir=projectDir)"
    result = successRun(projectDir=projectDir)
    if result != 0:
        r.addError(code)

    code = "failRun(projectDir=projectDir)"
    result = failRun(projectDir=projectDir)
    if result != 1:
        r.addError(code)

    code = "errorRun(projectDir=projectDir)"
    result = errorRun(projectDir=projectDir)
    if result != 2:
        r.addError(code)

    code = (
        "spyRun(grepArgs=grepArgs, projectDir=projectDir"
        ", reporter='some_reporter', silent=True)"
    )
    grepArgs = o(
        grep=["grep1", "grep2"], grepTests=["greptest1"], grepSuites=["grepsuite1"]
    )
    expectedCliGrepArgs = [
        "--grep",
        "grep1",
        "--grep",
        "grep2",
        "--grep-tests",
        "greptest1",
        "--grep-suites",
        "grepsuite1",
    ]
    result = spyRun(
        grepArgs=grepArgs, projectDir=projectDir, reporter="some_reporter", silent=True
    )

    passed = (
        result == 0
        and len(spyResult.args) == 1
        and spyResult.args[0]
        == [
            sys.executable,
            "-m",
            "po_simple_test._vendor.simple_test_process",
            "some_reporter",
            "True",
            *expectedCliGrepArgs,
        ]
        and spyResult.kwargs == {"cwd": projectDir}
    )
    if not passed:
        r.addError(code)

    return r
