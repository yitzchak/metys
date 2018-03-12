import base64
import mimetypes
import os


class GetResults(object):

    def __init__(self, doc):
        self.doc = doc

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        for chunk in self.doc.chunks:
            if chunk['type'] == 'code' and chunk['options']['results']:
                chunk['results'] = []
                for msg in chunk['messages']:
                    result = self.get_result(chunk, msg)
                    if result:
                        chunk['results'].append(result)

    def get_result(self, chunk, msg):
        if 'content' in msg and 'data' in msg['content']:
            for type in self.doc.types:
                if type['mime'] in msg['content']['data']:
                    data = msg['content']['data'][type['mime']]
                    result = {}
                    result.update(type)
                    result['data'] = self.save_external(chunk, type['mime'], data) if type['external'] else data
                    return result

    def save_external(self, chunk, mime, data):
        mode = 'w'
        if mime in ('application/pdf', 'image/png', 'image/jpeg'):
            data = base64.b64decode(data)
            mode = 'wb'
        name = chunk['options']['name'] + "-" + str(sum(1 for r in chunk['results'] if r['external'])+1)
        ext = mimetypes.guess_extension(mime)
        if ext:
            name += ext
        with open(os.path.join(self.doc.root, name), mode) as f:
            f.write(data)
        return name
