# ------- #
# Imports #
# ------- #

from textwrap import dedent
from traceback import format_exc
from types import SimpleNamespace as o
from .utils import twoLineSeps
import importlib


# ---- #
# Main #
# ---- #


def validateAndGetReportFn(argsObj, cliResult):
    validationResult = o(report=None, cliResult=cliResult, hasError=False)

    cliResult = validationResult.cliResult
    if argsObj.reporter.startswith("."):
        if not argsObj.silent:
            cliResult.stderr = dedent(
                f"""\
                relative module paths are not supported for the reporter
                reporter: {argsObj.reporter}
                """
            )

        cliResult.code = 2
        validationResult.hasError = True
        return validationResult

    try:
        reporterModule = importlib.import_module(argsObj.reporter)
    except:
        if not argsObj.silent:
            err = "An error occurred while importing the reporter"
            cliResult.stderr = err + twoLineSeps + format_exc()

        cliResult.code = 2
        validationResult.hasError = True
        return validationResult

    if hasattr(reporterModule, "report") and callable(reporterModule.report):
        validationResult.report = reporterModule.report
    else:
        if not argsObj.silent:
            cliResult.stderr = "the reporter must expose a callable 'report'"

        cliResult.code = 2
        validationResult.hasError = True

    return validationResult
