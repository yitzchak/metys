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
                if 'output' in chunk.options:
                    with open(chunk.options['output'], 'w+') as g:
                        g.write(chunk.output)
                else:
                    f.write(chunk.output)
