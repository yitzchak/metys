import re


class DeduceOptions:

    def __init__(self, doc):
        self.doc = doc

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        if 'parser' not in self.doc.options:
            if re.search(r'(?i)\..*nw$', self.doc.source):
                self.doc.options['parser'] = 'noweb'
            elif re.search(r'(?i)\..*md$', self.doc.source):
                self.doc.options['parser'] = 'markdown'
            else:
                self.doc.options['parser'] = 'metys'

        if 'format' not in self.doc.options:
            if re.search(r'(?i)\..*md$', self.doc.source):
                self.doc.options['format'] = 'markdown'
            else:
                self.doc.options['format'] = 'latex'

        if 'kernel' not in self.doc.options:
            if re.search(r'(?i)\.R(nw|md|mt)$', self.doc.source):
                self.doc.options['kernel'] = 'R'
            if re.search(r'(?i)\.P(nw|md|mt)$', self.doc.source):
                self.doc.options['kernel'] = 'python'
            else:
                self.doc.options['kernel'] = 'python'
