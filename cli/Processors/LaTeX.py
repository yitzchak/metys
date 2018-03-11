class LaTeX:

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self, chunks):
        for chunk in chunks:
            if 'results' in chunk:
                chunk['output'] = '\n'.join(map(lambda result: ('\\includegraphics{' + result['data'] + '}') if result['external'] else result['data'], chunk['results']))
            else:
                chunk['output'] = chunk['input']
