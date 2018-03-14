class ApplyDefaultOptions:

    def __init__(self, doc):
        self.doc = doc

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        for chunk in self.doc.chunks:
            options = {}
            options.update(self.doc.options)
            options.update(chunk.options)
            chunk.options = options
