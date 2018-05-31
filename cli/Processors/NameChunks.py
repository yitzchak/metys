class NameChunks:
    def __init__(self, root):
        self.root = root

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        counts = {}
        for chunk in self.root.chunks:
            if chunk.type in counts:
                counts[chunk.type] += 1
            else:
                counts[chunk.type] = 1
            if "name" not in chunk.options:
                chunk.options["name"] = (
                    self.root.options["name"]
                    + "-"
                    + chunk.type
                    + str(counts[chunk.type])
                )
            if chunk.type == "group":
                with NameChunks(chunk) as p:
                    p.apply()
