# ------- #
# Imports #
# ------- #

from copy import deepcopy
from simple_test_process.parseArgs import _grepArgs as emptyGrepArgs
from types import SimpleNamespace as o
from po.simple_test.cli.index import createRunSimpleTest, runSimpleTest
from po.simple_test.cli.usage import usage
from po.simple_test.fns import passThrough, raise_
from po.simple_test import version
import os


# ---- #
# Init #
# ---- #


successState = object()


def runSpySimpleTest(*args, **kwargs):
    spy = o()

    def spyRun(*, grepArgs, projectDir, reporter, silent):
        nonlocal spy
        spy = o(
            grepArgs=grepArgs,
            projectDir=projectDir,
            reporter=reporter,
            silent=silent,
        )
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
        and result.grepArgs == emptyGrepArgs
    )
    if not passed:
        r.addError(code)

    code = "runSpySimpleTest(['--grep', 'grep1', '--grep', 'grep2'])"
    result = runSpySimpleTest(["--grep", "grep1", "--grep", "grep2"])
    cliResult = result.cliResult
    expectedGrepArgs = deepcopy(emptyGrepArgs)
    expectedGrepArgs.grep.extend(["grep1", "grep2"])
    passed = (
        cliResult.stdout is None
        and cliResult.stderr is None
        and cliResult.code == 0
        and result.projectDir is None
        and result.reporter is None
        and result.silent is False
        and result.grepArgs == expectedGrepArgs
    )
    if not passed:
        r.addError(code)

    code = (
        "runSpySimpleTest("
        "['--grep-tests', 'grep1test', '--grep-suites', 'grep1suite']"
        ")"
    )
    result = runSpySimpleTest(
        ["--grep-tests", "grep1test", "--grep-suites", "grep1suite"]
    )
    cliResult = result.cliResult
    expectedGrepArgs = deepcopy(emptyGrepArgs)
    expectedGrepArgs.grepTests.append("grep1test")
    expectedGrepArgs.grepSuites.append("grep1suite")
    passed = (
        cliResult.stdout is None
        and cliResult.stderr is None
        and cliResult.code == 0
        and result.projectDir is None
        and result.reporter is None
        and result.silent is False
        and result.grepArgs == expectedGrepArgs
    )
    if not passed:
        r.addError(code)

    return r
