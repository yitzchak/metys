import base64
import mimetypes
import os
import re


class FormatOutput(object):

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
                chunk.output = self.format(chunk, 'text/plain', None, chunk.input)
            elif chunk.type == 'code':
                parts = []
                if chunk.options['echo']:
                    parts.append(self.format(chunk, chunk.language_info['mimetype'], chunk.language_info['pygments_lexer'], chunk.input))
                if chunk.options['results'] and hasattr(chunk, 'messages'):
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
                    return self.format(chunk, mimetype, None, content)
        return ''

    def format(self, chunk, mimetype, pygments_lexer, value):
        formatter = chunk.options['formatters'][chunk.options['format']]
        return formatter.format(chunk, mimetype, pygments_lexer, value)
