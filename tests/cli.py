# ------- #
# Imports #
# ------- #

from types import SimpleNamespace as o
from simple_test.cli.index import createRunSimpleTest, runSimpleTest, usage
from simple_test.fns import justReturn, passThrough, raise_
from simple_test import version
from simple_test.state import createEmptyState
from . import test_reporter_success
import os


# ---- #
# Init #
# ---- #


def successRun(*args, **kwargs):
    successState = createEmptyState()
    successState.testsFound = True

    if not kwargs["silent"] and kwargs["report"]:
        kwargs["report"](successState)

    return successState


def runSpySimpleTest(*args, **kwargs):
    spy = o()

    def spyRun(*, filesAndDirs, report, rootDir, silent):
        nonlocal spy
        spy = o(
            filesAndDirs=filesAndDirs,
            report=report,
            rootDir=rootDir,
            silent=silent,
        )
        successState = createEmptyState()
        successState.testsFound = True
        return successState

    spy.cliResult = createRunSimpleTest(spyRun)(*args, **kwargs)

    return spy


noopRun = justReturn(createEmptyState())
runNoopSimpleTest = createRunSimpleTest(noopRun)
runSuccessSimpleTest = createRunSimpleTest(successRun)
raiseError = lambda *args, **kwargs: raise_(Exception, "just an error")


# ---- #
# Main #
# ---- #


def runTests(r):
    return passThrough(r, [success, fail])


def fail(r):
    code = "runNoopSimpleTest(['--help', '--silent'])"
    result = runNoopSimpleTest(["--help", "--silent"])
    stderr = "'--help' must be the only argument when passed"
    if result.stderr != stderr or result.code != 2:
        r.addError(code)

    code = "runNoopSimpleTest([])"
    result = runNoopSimpleTest([])
    stderr = "at least one file or directory must be given"
    if result.stderr != stderr or result.code != 2:
        r.addError(code)

    code = "runNoopSimpleTest(['--invalid'])"
    result = runNoopSimpleTest(["--invalid"])
    stderr = "invalid option '--invalid'" + os.linesep + usage
    if result.stderr != stderr or result.code != 2:
        r.addError(code)

    code = "runNoopSimpleTest(['--reporter'])"
    result = runNoopSimpleTest(["--reporter"])
    stderr = "'--reporter' must be given a value" + os.linesep + usage
    if result.stderr != stderr or result.code != 2:
        r.addError(code)

    code = "runNoopSimpleTest(['--root-dir'])"
    result = runNoopSimpleTest(["--root-dir"])
    stderr = "'--root-dir' must be given a value" + os.linesep + usage
    if result.stderr != stderr or result.code != 2:
        r.addError(code)

    code = "runSimpleTest(raiseError, ['somefile'])"
    result = runSimpleTest(raiseError, ["somefile"])
    stderr = "simple-test ran into an issue when running"
    stderrIsExpected = (
        result.stderr.startswith(os.linesep + stderr)
        and "just an error" in result.stderr
    )
    if not stderrIsExpected or result.code != 4:
        r.addError(code)

    code = "runNoopSimpleTest(['someFile.py'])"
    result = runNoopSimpleTest(["someFile.py"])
    stderr = "No tests were found"
    if result.stderr != stderr or result.code != 3:
        r.addError(code)

    code = "runNoopSimpleTest(['--reporter', 'doesnt_exist', 'someFile'])"
    result = runNoopSimpleTest(["--reporter", "doesnt_exist", "someFile"])
    stderr = "An error occurred while importing the reporter"
    if not result.stderr.startswith(stderr) or result.code != 2:
        r.addError(code)

    code = (
        "runNoopSimpleTest(['--reporter', '.test_reporter_fail', 'someFile'])"
    )
    result = runNoopSimpleTest(
        ["--reporter", ".test_reporter_fail", "someFile"]
    )
    stderr = "relative module paths are not supported for the reporter"
    if not result.stderr.startswith(stderr) or result.code != 2:
        r.addError(code)

    code = (
        "runNoopSimpleTest(['--reporter',"
        " 'tests.test_reporter_fail', 'someFile'])"
    )
    result = runNoopSimpleTest(
        ["--reporter", "tests.test_reporter_fail", "someFile"]
    )
    stderr = "the reporter must expose a callable 'report'"
    if result.stderr != stderr or result.code != 2:
        r.addError(code)

    return r


def success(r):
    code = "runNoopSimpleTest(['--help'])"
    result = runNoopSimpleTest(["--help"])
    if result.stdout != usage or result.code != 0:
        r.addError(code)

    code = "runNoopSimpleTest(['--version'])"
    result = runNoopSimpleTest(["--version"])
    if result.stdout != version or result.code != 0:
        r.addError(code)

    code = (
        "runSuccessSimpleTest(['--reporter'"
        ", 'tests.test_reporter_success', 'someFile'])"
    )
    test_reporter_success.wasCalled = False
    result = runSuccessSimpleTest(
        ["--reporter", "tests.test_reporter_success", "someFile"]
    )
    if (
        result.stdout is not None
        or result.code != 0
        or not test_reporter_success.wasCalled
    ):
        r.addError(code)

    code = (
        "runSpySimpleTest(['--reporter'"
        ", 'tests.test_reporter_success', '--root-dir', 'tests'"
        ", '--silent', 'someFile1', 'someFile2'])"
    )
    result = runSpySimpleTest(
        [
            "--reporter",
            "tests.test_reporter_success",
            "--root-dir",
            "tests",
            "--silent",
            "someFile1",
            "someFile2",
        ]
    )
    cliResult = result.cliResult
    if (
        cliResult.stdout is not None
        or cliResult.code != 0
        or result.filesAndDirs != ["someFile1", "someFile2"]
        or result.rootDir != "tests"
        or result.report is not test_reporter_success.report
    ):
        r.addError(code)

    return r
