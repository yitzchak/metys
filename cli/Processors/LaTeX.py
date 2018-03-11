class LaTeX:

    def __init__(self, doc):
        self.doc = doc

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        for chunk in self.doc.chunks:
            if 'results' in chunk:
                chunk['output'] = '\n'.join(map(lambda result: ('\\includegraphics{' + result['data'] + '}') if result['external'] else result['data'], chunk['results']))
            else:
                chunk['output'] = chunk['input']
