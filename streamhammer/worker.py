
#import librtmp

from output import debugout, setProcessName
import output
import metadata

def worker(i, streamData):
    setProcessName("{0}[{1}]".format(metadata.package, i))
    debugout("start".format(i))

    streamUrl = streamData.getStreamUrl()
    debugout("stream url = {0}".format(streamUrl))

    debugout("stop")


if __name__ == '__main__':
    raise Exception("Can't run this file directly")
