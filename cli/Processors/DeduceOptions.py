import re


class DeduceOptions:
    def __init__(self, root):
        self.root = root

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        if self.root.type == "group":
            if "input" in self.root.options:
                input = self.root.options["input"]

                if "format" not in self.root.options:
                    if re.search(r"(?i)\..*md$", input):
                        self.root.options["format"] = "markdown"
                    else:
                        self.root.options["format"] = "latex"

                if "graphics_options" not in self.root.options:
                    self.root.options["graphics_options"] = {
                        "width": "\\linewidth"
                        if self.root.options["format"] == "latex"
                        else "100%"
                    }

                if "kernel" not in self.root.options:
                    if re.search(r"(?i)\.R(nw|md|mt)$", input):
                        self.root.options["kernel"] = "R"
                    if re.search(r"(?i)\.P(nw|md|mt)$", input):
                        self.root.options["kernel"] = "python"
                    else:
                        self.root.options["kernel"] = "python"

                if "mimetypes" not in self.root.options:
                    self.root.options["mimetypes"] = (
                        [
                            "application/pdf",
                            "image/png",
                            "image/jpeg",
                            "text/latex",
                            "text/plain",
                        ]
                        if self.root.options["format"] == "latex"
                        else [
                            "image/svg+xml",
                            "image/png",
                            "image/jpeg",
                            "text/latex",
                            "text/plain",
                        ]
                    )
            for chunk in self.root.chunks:
                with DeduceOptions(chunk) as p:
                    p.apply()
