import base64
import mimetypes
import os


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
        name = os.path.join(chunk.options['figure_path'], name)
        with open(name, mode) as f:
            f.write(value)
        return name

    def format(self, chunk, mimetype, value):
        return None


class LaTeXFormatter(Formatter):

    def format_options(self, options, key):
        if key not in options:
            return ''

        if isinstance(options[key], dict):
            return '[' + ', '.join(k + '=' + v for k, v in options[key].items()) + ']'
        return '[' + options[key] + ']'

    def format(self, chunk, mimetype, pygments_lexer, value):
        if mimetype in ('text/plain', 'text/latex', 'text/tex'):
            return value

        if mimetype in ('application/pdf', 'image/png', 'image/jpeg'):
            graphics_options = self.format_options(chunk.options, 'graphics_options')
            figure_env_options = self.format_options(chunk.options, 'figure_env_options')
            format_str = '\\includegraphics{2}{{{0}}}' if 'figure_caption' not in chunk.options else '\\begin{{{figure_env}}}{1}\n\\includegraphics{2}{{{0}}}\n\caption{{{figure_caption}}}\\label{{{figure_prefix}{name}}}\n\\end{{{figure_env}}}'
            name = self.save_external(chunk, mimetype, value)
            return format_str.format(name, figure_env_options, graphics_options, **chunk.options)

        if mimetype == 'text/x.latex-math':
            if chunk.options['wrap_math']:
                format_str = '\\({0}\\)' if chunk.options['inline'] else '\\begin{{{math_env}}}\n{0}\\label{{{math_prefix}{name}}}\n\\end{{{math_env}}}'
                return format_str.format(value, **chunk.options)
            return value

        code_env_options = self.format_options(chunk.options, 'code_env_options')

        if chunk.options['code_env'] == 'minted':
            format_str = '\\mintinline{1}{{{2}}}{{{0}}}' if chunk.options['inline'] else '\\begin{{minted}}{1}{{{2}}}\n{0}\n\\end{{minted}}'
            return format_str.format(value.strip('\n'), code_env_options, 'text' if pygments_lexer is None else pygments_lexer, **chunk.options)

        format_str = '\\begin{{{code_env}}}{1}\n{0}\n\\end{{{code_env}}}'
        return format_str.format(value.strip('\n'), code_env_options, **chunk.options)


class MarkDownFormatter(Formatter):

    def format(self, chunk, mimetype, pygments_lexer, value):
        if mimetype == 'text/plain':
            return value

        if mimetype in ('image/svg+xml', 'image/png', 'image/jpeg'):
            format_str = '[{0}]({figure_caption})'
            name = self.save_external(chunk, mimetype, value)
            return format_str.format(name, **chunk.options)

        if mimetype == 'text/x.latex-math':
            if chunk.options['wrap_math']:
                format_str = '${0}$' if chunk.options['inline'] else '$$\n{0}\n$$'
                return format_str.format(value, **chunk.options)
            return value

        format_str = '`{0}`' if chunk.options['inline'] else '```{kernel}\n{0}\n```'
        return format_str.format(value, **chunk.options)
