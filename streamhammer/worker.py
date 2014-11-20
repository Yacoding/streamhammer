
import cli
import metadata
from output import debugout, setProcessName
import timeutil

import datetime
import librtmp


class Worker:

    i = None
    streamData = None

    def __init__(self, i, streamData):
        self.i = i
        self.streamData = streamData

    def runRtmp(self, streamUrl):

        t = int(cli.settings['timeout'])

        debugout("connect RTMP: {0}".format(streamUrl))

        conn = librtmp.RTMP(url=streamUrl,
                            live=True,
                            timeout=t,
                            pageurl=metadata.url)
        conn.connect()
        stream = conn.create_stream()

        maxtime = int(cli.settings['for'])
        tstart = datetime.datetime.now()

        debugout("streaming: {0}".format(streamUrl))

        while True:
            data = stream.read(1024)
            tnow = datetime.datetime.now()
            tdiffms = timeutil.timediffms(tstart, tnow)
            if tdiffms > maxtime:
                debugout("disconnect: time limit exceeded")
                return


    def run(self):
        setProcessName("{0}[{1}]".format(metadata.package, self.i))
        debugout("start")

        streamUrl = self.streamData.getStreamUrl()

        if streamUrl.startswith('rtmp://'):
            self.runRtmp(streamUrl)
        else:
            raise Exception("Unknown stream type: {0}".format(streamUrl))

        debugout("stop")


def worker(i, streamData):
    app = Worker(i, streamData)
    app.run()


if __name__ == '__main__':
    raise Exception("Can't run this file directly")
