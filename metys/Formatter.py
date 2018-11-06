import base64
import mimetypes
import os
import re


class Formatter(object):
    def save_external(self, chunk, mimetype, value):
        mode = "w"
        if mimetype in ("application/pdf", "image/png", "image/jpeg"):
            value = base64.b64decode(value)
            mode = "wb"
        chunk.external_count += 1
        name = chunk.options["name"] + "-" + str(chunk.external_count)
        ext = mimetypes.guess_extension(mimetype)
        if ext:
            name += ext
        dir = os.path.join(chunk.options["root"], chunk.options["figure_path"])
        if not os.path.exists(dir):
            os.makedirs(dir)
        name = os.path.join(dir, name)
        print("[metys] Writing {0}".format(name))
        with open(name, mode) as f:
            f.write(value)
        return name

    def format(self, chunk, mimetype, value):
        return None


class LaTeXFormatter(Formatter):

    graphics_format = "\\includegraphics{graphics_options}{{{0}}}"

    figure_format = """\\begin{{{figure_env}}}{figure_env_options}
\\includegraphics{graphics_options}{{{0}}}
\\caption{{{figure_caption}}}
\\label{{{figure_prefix}{name}-{label_number}}}
\\end{{{figure_env}}}"""

    math_format = """\\begin{{{math_env}}}{math_env_options}
{0}{math_post}
\\label{{{math_prefix}{name}-{label_number}}}
\\end{{{math_env}}}"""

    inline_math_format = "\\({0}\\)"

    minted_format = """\\begin{{minted}}{verb_env_options}{{{pygments_lexer}}}
{0}
\\end{{minted}}"""

    inline_minted_format = "\\mintinline{verb_env_options}{{{pygments_lexer}}}{{{0}}}"

    verb_format = """\\begin{{{verb_env}}}{verb_env_options}
{0}
\\end{{{verb_env}}}"""

    def add_label(self, chunk, name):
        if hasattr(chunk, "labels"):
            if name in chunk.labels:
                chunk.labels[name] += 1
            else:
                chunk.labels[name] = 1
        else:
            chunk.labels = {}
            chunk.labels[name] = 1

        return chunk.labels[name]

    def format_options(self, options, key):
        opt_format = "[{0}]"

        if key not in options:
            options[key] = ""
        elif isinstance(options[key], dict):
            options[key] = opt_format.format(
                ", ".join(k + "=" + v for k, v in options[key].items())
            )
        else:
            options[key] = opt_format.format(options[key])

    def escape_characters(self, value):
        return re.sub(
            r"([&%$#_{}])",
            r"\\\1",
            value.replace("\\", "\\textbackslash ")
            .replace("~", "\\textasciitilde ")
            .replace("<", "\\textless ")
            .replace(">", "\\textgreater ")
            .replace("^", "\\textasciicircum "),
        )

    def format(self, chunk, mimetype, pygments_lexer, value):
        if mimetype == "text/plain":
            return self.escape_characters(value)

        if mimetype in ("text/latex", "text/x-latex", "text/tex", "text/x-tex"):
            return value

        options = chunk.options.copy()

        self.format_options(options, "code_env_options")
        self.format_options(options, "figure_env_options")
        self.format_options(options, "graphics_options")
        self.format_options(options, "stderr_env_options")
        self.format_options(options, "stdout_env_options")

        options["pygments_lexer"] = "text" if pygments_lexer is None else pygments_lexer

        if mimetype in ("application/pdf", "image/png", "image/jpeg"):
            format_str = (
                self.figure_format
                if "figure_caption" in options
                else self.graphics_format
            )
            value = self.save_external(chunk, mimetype, value)
            options["label_number"] = self.add_label(chunk, options["figure_prefix"])
        elif mimetype == "text/x.latex-math":
            if options["wrap_math"]:
                options["math_post"] = ""

                if "math_tag" in options:
                    number = options["math_tag"].format(
                        chunk.reply["content"]["execution_count"]
                    )
                    if options["math_env"] in ("dmath"):
                        if "math_env_options" in options:
                            options["math_env_options"]["number"] = number
                        else:
                            options["math_env_options"] = {"number": number}
                    else:
                        options["math_post"] = "\\tag{{{0}}}".format(number)

                if options["inline"]:
                    format_str = self.inline_math_format
                else:
                    format_str = self.math_format
                    options["label_number"] = self.add_label(
                        chunk, options["math_prefix"]
                    )
            else:
                return value
        else:
            if mimetype == "text/x.stderr":
                options["verb_env"] = options["stderr_env"]
                options["verb_env_options"] = options["stderr_env_options"]
            elif mimetype == "text/x.stdout":
                options["verb_env"] = options["stdout_env"]
                options["verb_env_options"] = options["stdout_env_options"]
            else:
                options["verb_env"] = options["code_env"]
                options["verb_env_options"] = options["code_env_options"]

            if options["verb_env"] == "minted":
                format_str = (
                    self.inline_minted_format
                    if options["inline"]
                    else self.minted_format
                )
            else:
                format_str = self.verb_format

        self.format_options(options, "math_env_options")

        return format_str.format(value.strip("\n"), **options)


class MarkDownFormatter(Formatter):
    def format(self, chunk, mimetype, pygments_lexer, value):
        print(mimetype)
        if mimetype == "text/plain" or mimetype == "text/markdown":
            return value

        if mimetype in ("image/svg+xml", "image/png", "image/jpeg"):
            format_str = "[{0}]({figure_caption})"
            name = self.save_external(chunk, mimetype, value)
            return format_str.format(name, **chunk.options)

        if mimetype == "text/x.latex-math":
            if chunk.options["wrap_math"]:
                format_str = "${0}$" if chunk.options["inline"] else "$$\n{0}\n$$"
                return format_str.format(value, **chunk.options)
            return value

        if mimetype == "text/x.stdout" or mimetype == "text/x.stderr":
            format_str = "`{0}`" if chunk.options["inline"] else "```\n{0}\n```"
            return format_str.format(value.strip("\n"))

        format_str = "`{0}`" if chunk.options["inline"] else "```{kernel}\n{0}\n```"
        return format_str.format(value.strip("\n"), **chunk.options)
