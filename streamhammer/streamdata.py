
from output import debugout

import urllib2
import json
from operator import itemgetter


class StreamData:

    opts = {}

    def __init__(self, opts):
        self.opts = opts

    def getManifest(self):
        url = self.opts.get('manifest')
        t = int(self.opts.get('timeout'))
        debugout("downloading manifest: {0}".format(url))
        data = urllib2.urlopen(url=url, timeout=t).read()
        debugout("manifest: {0}".format(data))
        manifest = json.loads(data)
        if len(manifest) == 0:
            raise Exception("Manifest is empty from {0}".format(url))
        # Sort it from highest bitrate to lowest
        sortedManifest = sorted(manifest, key=itemgetter('bitrate'), reverse=True)
        return sortedManifest

    def getStreamData(self):
        if self.opts.get('manifest') is None:
            raise Exception("Cannot getStreamData without a manifest")
        manifest = self.getManifest()
        maxBitrate = int(self.opts.get('max-bitrate-per-stream'))
        manifestLen = len(manifest)
        for i in xrange(0, manifestLen):
            entry = manifest[i]
            if maxBitrate > 0 and entry['bitrate'] <= maxBitrate:
                return entry
#            debugout("getStreamData: Ignore stream[{0}] bitrate {1}".format(i, entry['bitrate']))
        # No suitable bitrate was found, get the lowest we can
#        debugout("getStreamData: Return lowest quality stream")
        return manifest[manifestLen-1]

    def getStreamUrl(self):
        # If there is a single stream, return it
        stream = self.opts.get('stream')
        if stream is not None:
            return stream
        # Else get the manifest and return the best quality stream within the allowed bitrate
        streamData = self.getStreamData()
        return streamData['location']


if __name__ == '__main__':
    raise Exception("Can't execute this file directly")
