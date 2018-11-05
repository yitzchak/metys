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
            if chunk.type == "group":
                with FormatOutput(chunk) as p:
                    p.apply()
            elif chunk.type == "text":
                chunk.output = self.format(
                    chunk, "text/" + chunk.options["format"], None, chunk.input
                )
            elif chunk.type == "code":
                parts = []
                if chunk.options["code_echo"]:
                    input = chunk.input
                    if "prompt" in chunk.options:
                        input = (
                            chunk.options["prompt"].format(
                                chunk.reply["content"]["execution_count"]
                            )
                            + input
                        )
                    parts.append(
                        self.format(
                            chunk,
                            chunk.language_info["mimetype"],
                            chunk.language_info["pygments_lexer"],
                            input,
                        )
                    )
                if chunk.options["results"] and hasattr(chunk, "messages"):
                    for msg in chunk.messages:
                        parts.append(self.format_message(chunk, msg))
                chunk.output = (" " if chunk.options["inline"] else "\n").join(parts)

    def format_message(self, chunk, msg):
        if msg["msg_type"] in ("display_data", "execute_result"):
            for mimetype in chunk.options["mimetypes"]:
                if mimetype in msg["content"]["data"]:
                    content = msg["content"]["data"][mimetype]
                    if chunk.options["math_split"] and mimetype in (
                        "text/latex",
                        "text/x-latex",
                        "text/tex",
                        "text/x-tex",
                    ):
                        parts = re.split(r"(?s)(?P<d>[$]{1,2})(.*?)(?P=d)", content)
                        output = ""
                        for i in range(len(parts)):
                            sub = i % 3
                            if sub == 0:
                                output += self.format(
                                    chunk, "text/latex", None, parts[i]
                                )
                            elif sub == 2:
                                output += self.format(
                                    chunk, "text/x.latex-math", None, parts[i]
                                )
                        return output
                    return self.format(chunk, mimetype, None, content)
        elif (
            msg["msg_type"] == "stream"
            and chunk.options[msg["content"]["name"] + "_echo"]
        ):
            return self.format(
                chunk, "text/x." + msg["content"]["name"], None, msg["content"]["text"]
            )
        return ""

    def format(self, chunk, mimetype, pygments_lexer, value):
        formatter = chunk.options["formatters"][chunk.options["format"]]
        return formatter.format(chunk, mimetype, pygments_lexer, value)
