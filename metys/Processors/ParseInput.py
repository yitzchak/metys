import io
import os
import re
import shlex
import urllib

from ..Chunk import Chunk


class ParseInput(object):
    def __init__(self, root):
        self.root = root
        self.stack = [root]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def read(self):
        file_path = os.path.join(self.root.options["root"], self.root.options["input"])

        try:
            inputfile = io.open(file_path, "r", encoding="utf-8")
            self.root.input = inputfile.read()
            inputfile.close()
        except IOError:
            inputfile = urllib.request.urlopen(file_path)
            self.root.input = inputfile.read().decode("utf-8")
            inputfile.close()

    def add_chunk(self, type=None, input=None, options=None):
        opts = {}
        # opts.update(self.root.options)
        if options and isinstance(options, str):
            opts.update(self.parse_options(options))
        elif options:
            opts.update(options)

        if "input" in opts:
            if "root" not in opts:
                dir, base = os.path.split(opts["input"])
                if dir == "":
                    opts["root"] = self.root.options["root"]
                else:
                    opts["root"] = os.path.join(self.root.options["root"], dir)
                    opts["input"] = base

        chunk = Chunk(type, input, opts)
        self.stack[-1].chunks.append(chunk)

        if "input" in opts:
            with ParseInput(chunk) as p:
                p.apply()
        return chunk

    def start_chunk(self, type=None, input=None, options=None):
        chunk = self.add_chunk(type, input, options)
        self.stack.append(chunk)
        return chunk

    def end_chunk(self):
        self.stack.pop()

    def add_input(self, input):
        self.root.chunks[-1].input += input

    def parse_options(self, value):
        options = {}
        for match in re.finditer(
            r'(?s)(?P<name>\w+)(?:(?:\.(?P<sub>\w+))?\s*=\s*(?P<value>"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|[^,=\'"\s]*))?',
            value,
        ):
            if match.group("value") is None:
                options[self.default_key] = self.parse_value(match.group("name"))
            elif match.group("sub") is None:
                options[match.group("name")] = self.parse_value(match.group("value"))
            else:
                if match.group("name") not in options or not isinstance(
                    options[match.group("name")], dict
                ):
                    options[match.group("name")] = {}
                options[match.group("name")][match.group("sub")] = self.parse_value(
                    match.group("value")
                )

        return options

    def parse_value(self, value):
        if value.startswith('"') or value.startswith("'"):
            return shlex.split(value)[0]

        lv = value.lower()
        if lv == "true":
            return True
        elif lv == "false":
            return False
        elif lv == "none":
            return None
        else:
            return value

    def parse_metys(self):
        self.start_chunk(type="text")

        parts = re.split(r"(?s)(<\|(?:[^\\@|:]|\\.)*[@|:]|\|>)", self.root.input)
        for i in range(len(parts)):
            sub = i % 2
            if sub == 0:
                self.stack[-1].input += parts[i]
                self.end_chunk()
            elif parts[i] == "|>":
                self.start_chunk(type="text")
            else:
                chunk = self.start_chunk(
                    type="group" if parts[i][-1] == "@" else "code",
                    options=parts[i][2:-1].replace("\\@", "@").replace("\\|", "|").replace("\\:", ":"),
                )
                if parts[i][-1] == "|":
                    chunk.options["inline"] = True
                if chunk.type == "group":
                    self.start_chunk(type="text")

    def parse_noweb(self):
        self.add_chunk(type="text")
        parts = re.split(r"(?m)^(?:<<(.*?)>>=|@)\s*$", self.root.input)
        for i in range(len(parts)):
            sub = i % 2
            if sub == 0:
                self.add_input(parts[i])
            elif parts[i]:
                self.add_chunk(type="code", options=parts[i])
            else:
                self.add_chunk(type="text")

    def parse_markdown(self):
        parts = re.split(
            r"(?ms)(?P<fence>^```|(?<!`)`)\{([^}]+)\}(.*?)(?P=fence)", self.root.input
        )
        for i in range(len(parts)):
            sub = i % 4
            if sub == 0:
                self.add_chunk(type="text", input=parts[i])
            elif sub == 1:
                chunk = self.add_chunk(
                    type="code", input=parts[i + 2], options=parts[i + 1]
                )
                if parts[i] == "`":
                    chunk.options["inline"] = True

    def apply(self):
        file_path = os.path.join(self.root.options["root"], self.root.options["input"])
        print("[metys] Parsing {0}".format(file_path))

        self.read()

        if self.root.type == "group":
            if "parser" not in self.root.options:
                if re.search(r"(?i)\..*nw$", self.root.options["input"]):
                    self.root.options["parser"] = "noweb"
                elif re.search(r"(?i)\..*md$", self.root.options["input"]):
                    self.root.options["parser"] = "markdown"
                else:
                    self.root.options["parser"] = "metys"

            self.default_key = (
                "name" if self.root.options["parser"] == "noweb" else "kernel"
            )

            if self.root.options["parser"] == "noweb":
                self.parse_noweb()
            elif self.root.options["parser"] == "markdown":
                self.parse_markdown()
            else:
                self.parse_metys()
