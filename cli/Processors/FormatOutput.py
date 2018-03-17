import re


class FormatOutput(object):

    formats = {
        'latex': {
            'code': '\\begin{{verbatim}}\n{content}\n\\end{{verbatim}}',
            'application/pdf': '\\includegraphics{{{external}}}',
            'image/jpeg': '\\includegraphics{{{external}}}',
            'image/png': '\\includegraphics{{{external}}}',
            'text/x.latex-math': '\\begin{{equation}}\n{content}\\label{{eq:{name}}}\n\\end{{equation}}',
            'text/x.latex-math|inline': '${content}$'
        },
        'markdown': {
            'code': '```{kernel}\n{content}\n```',
            'code|inline': '`{content}`',
            'text/x.latex-math': '$$\n{content}\n$$',
            'text/x.latex-math|inline': '${content}$'
        },
        'minted': {
            'code': '\\begin{{minted}}{{{pygments_lexer}}}\n{content}\n\\end{{minted}}',
            'code|inline': '\\mintinline{{{pygments_lexer}}}{{{content}}}',
            'application/pdf': '\\includegraphics{{{external}}}',
            'image/jpeg': '\\includegraphics{{{external}}}',
            'image/png': '\\includegraphics{{{external}}}',
            'text/x.latex-math': '\\begin{{equation}}\n{content}\\label{{eq:{name}}}\n\\end{{equation}}',
            'text/x.latex-math|inline': '${content}$'
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
            elif chunk.type == 'text':
                chunk.output = self.format(chunk, 'text', content=chunk.input)
            elif chunk.type == 'code':
                parts = []
                if chunk.options['echo']:
                    pygments_lexer = chunk.language_info['pygments_lexer'] if hasattr(chunk, 'language_info') and 'pygments_lexer' in chunk.language_info else chunk.kernel
                    parts.append(self.format(chunk, 'code', pygments_lexer=pygments_lexer, content=chunk.input.strip('\n')))
                if chunk.type == 'code' and chunk.options['results'] and hasattr(chunk, 'messages'):
                    for msg in chunk.messages:
                        parts.append(self.format_message(chunk, msg))
                chunk.output = (' ' if chunk.options['inline'] else '\n').join(parts)

    def format_message(self, chunk, msg):
        if 'content' in msg and 'data' in msg['content']:
            for mimetype in chunk.options['mimetypes']:
                if mimetype in msg['content']['data']:
                    content = msg['content']['data'][mimetype]
                    if mimetype == 'text/latex':
                        match = re.match(r'(?s)^\s*[$]{1,2}(.*?)[$]{1,2}\s*$', content)
                        mimetype = 'text/x.latex-math'
                        content = match.group(1)
                    return self.format(chunk, mimetype, content=content)
        return ''

    def format(self, chunk, type, **kwargs):
        kwargs.update(chunk.options)
        f = self.formats[chunk.options['format']]
        if chunk.options['inline']:
            key = type + '|inline'
            if key in f:
                if '{external}' in f[key]:
                    kwargs['external'] = self.save_external(chunk, type, kwargs['content'])
                return f[key].format(**kwargs)
        return f[type].format(**kwargs) if type in f else kwargs['content']

    def save_external(self, chunk, mime, data):
        mode = 'w'
        if mime in ('application/pdf', 'image/png', 'image/jpeg'):
            data = base64.b64decode(data)
            mode = 'wb'
        name = chunk.options['name'] + "-" + str(sum(1 for r in chunk.results if r['external'])+1)
        ext = mimetypes.guess_extension(mime)
        if ext:
            name += ext
        with open(os.path.join('.', name), mode) as f:
            f.write(data)
        return name
