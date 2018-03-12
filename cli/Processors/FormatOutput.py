class FormatOutput:

    def __init__(self, doc):
        self.doc = doc

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        for chunk in self.doc.chunks:
            if chunk['type'] == 'code':
                chunk['output'] = ''
                self.output_code(chunk)
                self.output_results(chunk)
            else:
                chunk['output'] = chunk['input']

    def output_code(self, chunk):
        if chunk['options']['echo']:
            chunk['output'] += '\\begin{verbatim}\n' + chunk['input'] + '\n\\end{verbatim}\n'

    def output_results(self, chunk):
        if chunk['options']['results']:
                chunk['output'] += '\n'.join(map(lambda result: ('\\includegraphics{' + result['data'] + '}') if result['external'] else result['data'], chunk['results']))
