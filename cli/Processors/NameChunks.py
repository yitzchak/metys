class NameChunks:

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self, chunks):
        counts = {}
        for chunk in chunks:
            if chunk['type'] in counts:
                counts[chunk['type']] += 1
            else:
                counts[chunk['type']] = 1
            if 'name' not in chunk['options']:
                chunk['options']['name'] = chunk['type'] + str(counts[chunk['type']])
