import os


class Document(object):
    def __init__(self, source):
        self.source = source
        self.root = os.path.dirname(source)
        self.chunks = []
        self.options = {
            'kernel': 'python',
            'echo': True,
            'hidden': False
        }
        self.types = [
            {'mime': 'application/pdf', 'external': True},
            {'mime': 'image/png', 'external': True},
            {'mime': 'image/jpeg', 'external': True},
            {'mime': 'text/latex', 'external': False},
            {'mime': 'text/plain', 'external': False}
        ]
