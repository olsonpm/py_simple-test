from . import cli, run
from .Results import Results


def runTests():
    cli.runTests(Results("cli")).printResults()
    run.runTests()


__all__ = ["runTests"]
