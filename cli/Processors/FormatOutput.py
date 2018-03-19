import base64
import mimetypes
import os
import re


class Formatter(object):

    def save_external(self, chunk, mimetype, value):
        mode = 'w'
        if mimetype in ('application/pdf', 'image/png', 'image/jpeg'):
            value = base64.b64decode(value)
            mode = 'wb'
        chunk.external_count += 1
        name = chunk.options['name'] + "-" + str(chunk.external_count)
        ext = mimetypes.guess_extension(mimetype)
        if ext:
            name += ext
        with open(os.path.join('.', name), mode) as f:
            f.write(value)
        return name

    def format(self, chunk, mimetype, value):
        return None


class LaTeXFormatter(Formatter):

    def format(self, chunk, mimetype, pygments_lexer, value):
        if mimetype == 'text/plain':
            return value

        if mimetype in ('application/pdf', 'image/png', 'image/jpeg'):
            format_str = '\\includegraphics{{{0}}}' if chunk.options['figure_env'] is None or 'caption' not in chunk.options else '\\begin{{{figure_env}}}\n\\includegraphics{{{0}}}\n\caption{{{caption}}}\\label{{fig:{name}}}\n\\end{{{figure_env}}}'
            name = self.save_external(chunk, mimetype, value)
            return format_str.format(name, **chunk.options)

        if mimetype == 'text/x.latex-math':
            if chunk.options['math_env'] is None:
                return value
            format_str = '\\({0}\\)' if chunk.options['inline'] else '\\begin{{{math_env}}}\n{0}\\label{{eq:{name}}}\n\\end{{{math_env}}}'
            return format_str.format(value, **chunk.options)

        if chunk.options['code_env'] == 'minted' and pygments_lexer is not None:
            format_str = '\\mintinline{{{1}}}{{{0}}}' if chunk.options['inline'] else '\\begin{{minted}}{{{1}}}\n{0}\n\\end{{minted}}'
            return format_str.format(value, pygments_lexer, **chunk.options)

        format_str = '\\begin{{verbatim}}\n{0}\n\\end{{verbatim}}'
        return format_str.format(value, **chunk.options)


class MarkDownFormatter(Formatter):

    def format(self, chunk, mimetype, pygments_lexer, value):
        if mimetype == 'text/plain':
            return value

        if mimetype in ('image/svg+xml', 'image/png', 'image/jpeg'):
            format_str = '[{0}]({caption})'
            name = self.save_external(chunk, mimetype, value)
            return format_str.format(name, **chunk.options)

        if mimetype == 'text/x.latex-math':
            if chunk.options['math_env'] is None:
                return value
            format_str = '${0}$' if chunk.options['inline'] else '$$\n{0}\n$$'
            return format_str.format(value, **chunk.options)

        format_str = '`{0}`' if chunk.options['inline'] else '```{kernel}\n{0}\n```'
        return format_str.format(value, **chunk.options)



class FormatOutput(object):

    formatters = {
        'latex': LaTeXFormatter(),
        'markdown': MarkDownFormatter()
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
        formatter = self.formatters[chunk.options['format']]
        return formatter.format(chunk, mimetype, pygments_lexer, value)
