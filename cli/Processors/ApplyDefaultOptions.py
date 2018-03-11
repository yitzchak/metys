class ApplyDefaultOptions:

    def __init__(self, options):
        self.options = options

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self, chunks):
        for chunk in chunks:
            options = {}
            options.update(self.options)
            options.update(chunk['options'])
            chunk['options'] = options
