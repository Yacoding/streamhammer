
from streamdata import StreamData
import timeutil
from worker import worker
from output import debugout
import metadata

#import librtmp
from multiprocessing import Process
import datetime
import urllib2
import json
from operator import itemgetter


DEFAULT_MAX_CHILDREN = 1
DEFAULT_WAIT_MS = 0  # 0 means don't wait
DEFAULT_STARTUP_COUNT = 1  # start 1 at a time
MIN_CLEANUP_TIME = 100


class App:

    opts = {}
    streamData = None
    children = []

    def __init__(self, opts):
        self.opts = opts
        self.streamData = StreamData(opts)

    def cleanup(self):
        offset = 0
        max = len(self.children)
        for n in xrange(0, max):
            i = n - offset
            if not self.children[i]['p'].is_alive():
                debugout("child {0} @{1} finished".format(self.children[i]['n'], i))
                del self.children[i]
                offset = offset + 1
        cleaned = max - len(self.children)
        if cleaned > 0:
            debugout("cleanup: {0}/{1} cleaned".format(max-len(self.children), max))

    def waitAll(self):
        while len(self.children) > 0:
            self.cleanup()
            timeutil.microsleep(100000)

    def spawnGroup(self, i):
        max = int(self.opts.get('max', DEFAULT_MAX_CHILDREN))
        start = int(self.opts.get('start', DEFAULT_STARTUP_COUNT))
        for j in xrange(0, start):
            i += 1
            if i > max:
                break
            p = Process(target=worker, args=(i, self.streamData,))
            p.daemon = True
            p.name = '{0}[{1}]'.format(metadata.package, i)
            p.start()
            self.children.append({'n': i, 'p': p})
        return i

    def run(self):
        i = 0
        max = int(self.opts.get('max', DEFAULT_MAX_CHILDREN))
        everyms = int(self.opts.get('every', DEFAULT_WAIT_MS))
        while i < max:

            tstart = datetime.datetime.now()
            i = self.spawnGroup(i)
            tstop = datetime.datetime.now()

            tdiffms = timeutil.timediffms(tstart, tstop)
            tpausems = everyms - tdiffms

            # We should wait before we spawn any more streams
            if tpausems > 0:
                # If we have enough time to try cleaning up, then clean up
                if tpausems >= MIN_CLEANUP_TIME:
                    self.cleanup()
                    tstop = datetime.datetime.now()
                    tdiffms = timeutil.timediffms(tstart, tstop)
                    tpausems = int(self.opts['every']) - tdiffms
                # If we still have time to wait, then wait
                if tpausems > 0:
                    debugout("usleep {0}".format(tpausems))
                    timeutil.microsleep(tpausems * 1000)

        # All children have been spawned. Wait for them to finish.
        self.waitAll()


if __name__ == '__main__':
    raise Exception("Can't execute this file directly")
