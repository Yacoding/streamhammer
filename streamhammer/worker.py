
import cli
import metadata
from output import debugout, errorout, setProcessName
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

        try:
            t = int(cli.settings['timeout'])
            debugout("connect RTMP: {0}".format(streamUrl))
            conn = librtmp.RTMP(url=streamUrl,
                                live=True,
                                timeout=t,
                                pageurl=metadata.url)
            conn.connect()
        except Exception as e:
            errorout("RTMP Connection Error: {0}".format(e.message))
            return 1

        try:
            stream = conn.create_stream()
        except Exception as e:
            errorout("RTMP Create Stream: {0}".format(e.message))
            return 1

        maxtime = int(cli.settings['for'])
        tstart = datetime.datetime.now()

        try:
            debugout("streaming: {0}".format(streamUrl))

            while True:
                data = stream.read(16*1024)
                tnow = datetime.datetime.now()
                tdiffms = timeutil.timediffms(tstart, tnow)
                if tdiffms > maxtime:
                    debugout("disconnect: time limit reached")
                    return 0
        except Exception as e:
            errorout("RTMP Streaming Error: {0}".format(e.message))

        return 1


    def run(self):
        setProcessName("{0}[{1}]".format(metadata.package, self.i))
        debugout("start")

        try:
            streamUrl = self.streamData.getStreamUrl()
        except Exception as e:
            debugout("stop cannot find stream url")
            return 1

        r = 0

        if streamUrl.startswith('rtmp://'):
            r = self.runRtmp(streamUrl)
        else:
            raise Exception("Unknown stream type: {0}".format(streamUrl))

        debugout("stop")
        return r


def worker(i, streamData):
    app = Worker(i, streamData)
    app.run()


if __name__ == '__main__':
    raise Exception("Can't run this file directly")
