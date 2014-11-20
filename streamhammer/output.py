
from __future__ import print_function

import cli
import metadata

import sys

process_name = metadata.package

def setProcessName(name):
    global process_name
    process_name = name

def debugout(s):
    if not cli.settings['quiet']:
        sys.stderr.flush()
        print("{0}: {1}".format(process_name, s))
        sys.stdout.flush()

def errorout(s):
    print("ERROR: {0}: {1}".format(process_name, s), file=sys.stderr)
    sys.stderr.flush()
