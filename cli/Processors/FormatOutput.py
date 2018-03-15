import re


class FormatOutput:

    formats = {
        'latex': {
            'code': '\\begin{{verbatim}}\n{content}\n\\end{{verbatim}}\n',
            'external': '\\includegraphics{{{content}}}',
            'math': '\\begin{{equation}}\n{content}\\label{{eq:{name}}}\n\\end{{equation}}\n',
            'inline_math': '${content}$'
        },
        'markdown': {
            'code': '```{kernel}\n{content}\n```\n',
            'inline_code': '`{content}`',
            'math': '$$\n{content}\n$$\n',
            'inline_math': '${content}$'
        },
        'minted': {
            'code': '\\begin{{minted}}{{{pygments_lexer}}}\n{content}\n\\end{{minted}}\n',
            'inline_code': '\\mintinline{{{pygments_lexer}}}{{{content}}}',
            'external': '\\includegraphics{{{content}}}',
            'math': '\\begin{{equation}}\n{content}\n\\end{{equation}}\n',
            'inline_math': '${content}$'
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
                chunk.output = chunk.output.strip('\n')
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
            for result in chunk.results:
                if result['external']:
                    chunk.output += '\n' + self.format(chunk, 'external', content=result['data'])
                elif result['mime'] == 'text/latex':
                    match = re.match(r'(?s)^\s*[$]{1,2}(.*?)[$]{1,2}\s*$', result['data'])
                    if match:
                        chunk.output += '\n' + self.format(chunk, 'math', content=match.group(1))
                    else:
                        chunk.output += '\n' + self.format(chunk, 'text', content=result['data'])
                else:
                    chunk.output += '\n' + self.format(chunk, 'text', content=result['data'])
