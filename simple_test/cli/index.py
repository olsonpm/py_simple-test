#
# TODO: decide whether this should capture reporter output and assign it
#   to stdout
#


# ------- #
# Imports #
# ------- #

from ..meta import version
from traceback import format_exc
from textwrap import dedent
from types import SimpleNamespace as o
from ..fns import iif, isEmpty, isSomething
from .utils import twoLineSeps
from .validateAndGetReportFn import validateAndGetReportFn
import os


# ---- #
# Init #
# ---- #

arguments = set(["--reporter", "--root-dir", "--silent"])
helpOrVersion = set(["--help", "--version"])

usage = dedent(
    f"""
    Usage
      simple-test [options] <path to file or dir> [more paths..]
      simple-test (--help | --version)

    Options
      --root-dir  the root dir from which relative paths are figured.  Defaults
                  to `os.getcwd()`
      --silent    a flag which disables output
      --reporter  module name with a 'report' function.  The default reporter is
                  'simple_test_default_reporter'.  Relative modules e.g.
                  "..myModule" are not yet supported.

    Returns an exit code of
      0 for a successful run
      1 for a failed run
      2 if invalid arguments were given
      3 if simple-test couldn't find any tests
      4 if the run couldn't finish due to an exception
    """
)


# ---- #
# Main #
# ---- #


def createRunSimpleTest(run):
    return lambda args: runSimpleTest(run, args)


def runSimpleTest(run, args):
    result = o(stdout=None, stderr=None, code=None)

    numArgs = len(args)
    if numArgs == 1:
        if args[0] == "--help":
            result.stdout = usage
            result.code = 0
            return result
        elif args[0] == "--version":
            result.stdout = version
            result.code = 0
            return result

    validationResult = validateAndParseArgs(args, result)

    if validationResult.hasError:
        return validationResult.cliResult

    argsObj = validationResult.argsObj
    isSilent = argsObj.silent

    listOfFilesAndDirs = validationResult.positionalArgs
    if isEmpty(listOfFilesAndDirs):
        if not isSilent:
            result.stderr = "at least one file or directory must be given"

        result.code = 2
        return result

    report = None
    if isSomething(argsObj.reporter):
        validationResult = validateAndGetReportFn(argsObj, result)

        if validationResult.hasError:
            return validationResult.cliResult
        else:
            report = validationResult.report

    try:
        testResults = run(
            filesAndDirs=listOfFilesAndDirs,
            report=report,
            rootDir=argsObj.rootDir,
            silent=isSilent,
        )

        if not testResults.testsFound:
            if not isSilent:
                result.stderr = "No tests were found"

            result.code = 3
        else:
            result.code = iif(testResults.succeeded, 0, 1)

        return result

    except Exception:
        if not isSilent:
            err = dedent(
                f"""
                simple-test ran into an issue when running the tests and
                couldn't complete
                """
            )
            result.stderr = err + twoLineSeps + format_exc()

        result.code = 4
        return result


# ------- #
# Helpers #
# ------- #


def validateAndParseArgs(args, cliResult):
    argsObj = o(reporter=None, rootDir=None, silent=False)
    validationResult = o(
        argsObj=argsObj, cliResult=cliResult, hasError=False, positionalArgs=[]
    )

    i = 0

    while i < len(args):
        if not args[i].startswith("--"):
            break

        arg = args[i]
        if arg not in arguments:
            if not argsObj.silent:
                if arg in helpOrVersion:
                    cliResult.stderr = (
                        f"'{arg}' must be the only argument when passed"
                    )
                else:
                    cliResult.stderr = f"invalid option '{arg}'"
                    cliResult.stderr += os.linesep + usage

            cliResult.code = 2
            validationResult.hasError = True

            return validationResult

        if arg == "--silent":
            argsObj.silent = True
        elif arg == "--reporter":
            if i == len(args) - 1:
                if not argsObj.silent:
                    cliResult.stderr = "'--reporter' must be given a value"
                    cliResult.stderr += os.linesep + usage

                cliResult.code = 2
                validationResult.hasError = True
                return validationResult

            i += 1
            arg = args[i]
            argsObj.reporter = arg
        elif arg == "--root-dir":
            if i == len(args) - 1:
                if not argsObj.silent:
                    cliResult.stderr = "'--root-dir' must be given a value"
                    cliResult.stderr += os.linesep + usage

                cliResult.code = 2
                validationResult.hasError = True
                return validationResult

            i += 1
            arg = args[i]
            argsObj.rootDir = arg

        i += 1

    validationResult.positionalArgs = args[i:]

    return validationResult
