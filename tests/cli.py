# ------- #
# Imports #
# ------- #

from types import SimpleNamespace as o
from simple_test.cli.index import createRunSimpleTest, runSimpleTest
from simple_test.cli.usage import usage
from simple_test.fns import passThrough, raise_
from simple_test import version
import os


# ---- #
# Init #
# ---- #


successState = object()


def runSpySimpleTest(*args, **kwargs):
    spy = o()

    def spyRun(*, projectDir, reporter, silent):
        nonlocal spy
        spy = o(projectDir=projectDir, reporter=reporter, silent=silent)
        return 0

    spy.cliResult = createRunSimpleTest(spyRun)(*args, **kwargs)

    return spy


noopRun = lambda: True
runNoopSimpleTest = createRunSimpleTest(noopRun)
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

    code = "runNoopSimpleTest(['--project-dir'])"
    result = runNoopSimpleTest(["--project-dir"])
    stderr = "'--project-dir' must be given a value" + os.linesep + usage
    if result.stderr != stderr or result.code != 2:
        r.addError(code)

    code = "runNoopSimpleTest(['no', 'positional', 'args'])"
    result = runNoopSimpleTest(["no", "positional", "args"])
    stderr = (
        "this command doesn't take positional arguments" + os.linesep + usage
    )
    if result.stderr != stderr or result.code != 2:
        r.addError(code)

    code = "runSimpleTest(raiseError, [])"
    result = runSimpleTest(raiseError, [])
    stderr = "An unexpected error occurred"
    stderrIsExpected = (
        result.stderr.startswith(stderr) and "just an error" in result.stderr
    )
    if not stderrIsExpected or result.code != 2:
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
        "runSpySimpleTest(['--reporter'"
        ", 'tests.test_reporter_success', '--project-dir', 'tests'"
        ", '--silent'])"
    )
    result = runSpySimpleTest(
        [
            "--reporter",
            "tests.test_reporter_success",
            "--project-dir",
            "/myProject",
            "--silent",
        ]
    )
    cliResult = result.cliResult
    passed = (
        cliResult.stdout is None
        and cliResult.stderr is None
        and cliResult.code == 0
        and result.projectDir == "/myProject"
        and result.reporter == "tests.test_reporter_success"
        and result.silent is True
    )
    if not passed:
        r.addError(code)

    return r
