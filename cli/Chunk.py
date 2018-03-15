class Chunk(object):
    def __init__(self, type=None, input=None, options=None):
        self.options = {}
        self.type = type
        if options:
            self.options.update(options)
        self.input = input if input else ''
        self.chunks = []

    def __str__(self):
        if self.type == 'group':
             return self.type + '|' + str(self.options) + ';'.join(map(lambda x: str(x),self.chunks))
        else:
            return self.type + '|'  + str(self.options) + self.input
