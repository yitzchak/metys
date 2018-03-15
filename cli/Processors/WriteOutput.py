import os


class WriteOutput:

    def __init__(self, root):
        self.root = root
        if 'output' not in self.root.options:
            name, _ = os.path.splitext(self.root.options['source'])
            root.options['output'] = name + '.tex'

    def __enter__(self):
        self.file = open(self.root.options['output'], 'w+')
        return self

    def __exit__(self, type, value, traceback):
        self.file.close()
        pass

    def apply(self):
        for chunk in self.root.chunks:
            self.write_chunk(chunk)

    def write_chunk(self, chunk):
        if 'output' in chunk.options:
            with WriteOutput(chunk) as p:
                p.apply()
        elif chunk.type == 'group':
            for ch in chunk.chunks:
                self.write_chunk(ch)
        elif hasattr(chunk, 'output'):
            self.file.write(chunk.output)
