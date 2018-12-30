#! /usr/bin/env python

import sys
from .cli import runSimpleTest
from .run import run


def printErr(msg):
    print(msg, file=sys.stderr)


result = runSimpleTest(run, sys.argv[1:])

if result.stdout:
    print(result.stdout)

if result.stderr:
    print(result.stderr)

exit(result.code)
