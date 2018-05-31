class ApplyDefaultOptions:
    def __init__(self, root):
        self.root = root

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        for chunk in self.root.chunks:
            options = {}
            options.update(
                {
                    k: v
                    for k, v in self.root.options.items()
                    if k not in ("input", "output", "name")
                }
            )
            options.update(chunk.options)
            chunk.options = options
            if chunk.type == "group":
                with ApplyDefaultOptions(chunk) as p:
                    p.apply()
