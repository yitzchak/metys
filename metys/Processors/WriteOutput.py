import os


class WriteOutput:
    def __init__(self, root):
        self.root = root
        if "output" not in self.root.options:
            name, _ = os.path.splitext(self.root.options["input"])
            root.options["output"] = name + (
                ".md" if self.root.options["format"] == "markdown" else ".tex"
            )

    def __enter__(self):
        file_path = os.path.join(self.root.options["root"], self.root.options["output"])
        self.file = open(file_path, "w+")
        return self

    def __exit__(self, type, value, traceback):
        self.file.close()
        pass

    def apply(self):
        file_path = os.path.join(self.root.options["root"], self.root.options["output"])
        print("[metys] Writing {0}".format(file_path))
        for chunk in self.root.chunks:
            self.write_chunk(chunk)

    def write_chunk(self, chunk):
        if "output" in chunk.options:
            with WriteOutput(chunk) as p:
                p.apply()
        elif chunk.type == "group":
            for ch in chunk.chunks:
                self.write_chunk(ch)
        elif hasattr(chunk, "output"):
            self.file.write(chunk.output)
