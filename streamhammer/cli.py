
from app import App

from optparse import OptionParser


DEFAULT_OPTIONS = {
    'start': 1,
    'every': 1000,
    'max': 1,
    'max-bitrate-per-stream': 100000, # 0 means NO MAXIMUM
    'timeout': 10,
}


class Options(dict):

    def parseOptions(self):
        parser = OptionParser()
        parser.add_option("--start", dest="start")
        parser.add_option("--every", dest="every")
        parser.add_option("--max", dest="max")
        parser.add_option("--manifest", dest="manifest")
        parser.add_option("--stream", dest="stream")
        parser.add_option("--max-bitrate-per-stream", dest="max-bitrate-per-stream")
        parser.add_option("--timeout", dest="timeout")
        (opts, args) = parser.parse_args()

        # Convert opts to a dict, store in self
        for k, v in opts.__dict__.iteritems():
            if not callable(v) and not k.startswith('__'):
                if v is not None:
                    self[k] = v

    def assignDefaults(self):
        for n in DEFAULT_OPTIONS:
            if self.get(n) is None:
                self[n] = DEFAULT_OPTIONS[n]

    def sanityCheck(self):
        stream = self.get('stream')
        manifest = self.get('manifest')

        # Check for either stream or manifest ...
        if stream is None and manifest is None:
            raise Exception("Either --stream or --manifest is required")

        # ... but not both
        elif stream is not None and manifest is not None:
            raise Exception("Cannot use both --stream and --manifest")

    def __init__(self):
        dict.__init__(self)
        self.parseOptions()
        self.assignDefaults()
        self.sanityCheck()


def main():
    opts = Options()
    app = App(opts)
    app.run()


if __name__ == '__main__':
    main()
