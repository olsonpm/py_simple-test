# ------- #
# Imports #
# ------- #

from os import path
from po.simple_test.fns import justReturn
from po.simple_test.run import createRun
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
        "spyRun(projectDir=projectDir, reporter='some_reporter', silent=True)"
    )
    result = spyRun(
        projectDir=projectDir, reporter="some_reporter", silent=True
    )
    passed = (
        result == 0
        and len(spyResult.args) == 1
        and spyResult.args[0]
        == [
            sys.executable,
            "-m",
            "simple_test_process",
            projectDir,
            "some_reporter",
            "True",
        ]
        and spyResult.kwargs == {"cwd": projectDir}
    )
    if not passed:
        r.addError(code)

    return r
