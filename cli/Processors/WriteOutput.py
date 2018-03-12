import os


class WriteOutput:

    def __init__(self, doc):
        self.doc = doc

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        name, _ = os.path.splitext(self.doc.source)
        with open(name + '.tex', 'w+') as f:
            for chunk in self.doc.chunks:
                f.write(chunk['output'])
