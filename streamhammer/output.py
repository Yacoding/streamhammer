
import sys
import metadata

process_name = metadata.package

def setProcessName(name):
    global process_name
    process_name = name

def debugout(s):
    sys.stderr.flush()
    print "{0}: {1}".format(process_name, s)
    sys.stdout.flush()
