class WriteOutput:

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self, chunks):
        with open('test.tex', 'w+') as f:
            for chunk in chunks:
                f.write(chunk['output'])
