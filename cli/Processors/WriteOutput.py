class WriteOutput:

    def __init__(self, doc):
        self.doc = doc

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        with open('test.tex', 'w+') as f:
            for chunk in self.doc.chunks:
                f.write(chunk['output'])
