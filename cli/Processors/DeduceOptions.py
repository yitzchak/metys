import re


class DeduceOptions:

    def __init__(self, root):
        self.root = root

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def apply(self):
        source = self.root.options['source']
        # if 'parser' not in self.root.options:
        #     if re.search(r'(?i)\..*nw$', source):
        #         self.root.options['parser'] = 'noweb'
        #     elif re.search(r'(?i)\..*md$', source):
        #         self.root.options['parser'] = 'markdown'
        #     else:
        #         self.root.options['parser'] = 'metys'

        if 'format' not in self.root.options:
            if re.search(r'(?i)\..*md$', source):
                self.root.options['format'] = 'markdown'
            else:
                self.root.options['format'] = 'latex'

        if 'kernel' not in self.root.options:
            if re.search(r'(?i)\.R(nw|md|mt)$', source):
                self.root.options['kernel'] = 'R'
            if re.search(r'(?i)\.P(nw|md|mt)$', source):
                self.root.options['kernel'] = 'python'
            else:
                self.root.options['kernel'] = 'python'
