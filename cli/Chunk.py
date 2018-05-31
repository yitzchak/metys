class Chunk(object):
    def __init__(self, type=None, input=None, options=None):
        self.options = {}
        self.type = type
        if options:
            self.options.update(options)
        self.input = input if input else ""
        self.external_count = 0
        self.chunks = []
