class FormatOutput:

    formats = {
        'latex': {
            'code': '\\begin{{verbatim}}\n{content}\n\\end{{verbatim}}\n',
            'external': '\\includegraphics{{{content}}}'
        },
        'markdown': {
            'code': '```{kernel}\n{content}\n```\n',
            'inline_code': '`{content}`'
        },
        'minted': {
            'code': '\\begin{{minted}}{{{pygments_lexer}}}\n{content}\n\\end{{minted}}\n',
            'inline_code': '\\mintinline{{{pygments_lexer}}}{{{content}}}',
            'external': '\\includegraphics{{{content}}}'
        },
    }

    def __init__(self, root):
        self.root = root

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        for chunk in self.root.chunks:
            if chunk.type == 'group':
                with FormatOutput(chunk) as p:
                    p.apply()
            elif chunk.type == 'code':
                chunk.output = ''
                self.output_code(chunk)
                self.output_results(chunk)
            else:
                chunk.output = self.format(chunk, 'text', content=chunk.input)

    def format(self, chunk, type, **kwargs):
        kwargs.update(chunk.options)
        f = self.formats[chunk.options['format']]
        if chunk.options['inline']:
            key = 'inline_' + type
            if key in f:
                return f[key].format(**kwargs)
        return f[type].format(**kwargs) if type in f else kwargs['content']

    def output_code(self, chunk):
        if chunk.options['echo']:
            pygments_lexer = chunk.language_info['pygments_lexer'] if hasattr(chunk, 'language_info') and 'pygments_lexer' in chunk.language_info else chunk.kernel
            chunk.output += self.format(chunk, 'code', pygments_lexer=pygments_lexer, content=chunk.input.strip('\n'))

    def output_results(self, chunk):
        if chunk.options['results'] and hasattr(chunk, 'results'):
            chunk.output += '\n'.join(map(lambda result: self.format(chunk, 'external' if result['external'] else 'text', content=result['data']), chunk.results))
