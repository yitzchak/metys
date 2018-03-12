import io
import re
import shlex
import urllib

class ParseInput(object):

    def __init__(self, doc):
        self.doc = doc

    def __enter__(self):
        self.default_key = 'name' if self.doc.options['parser'] == 'noweb' else 'kernel'
        self.read()
        return self

    def __exit__(self, type, value, traceback):
        pass

    def read(self):
        try:
            sourcefile = io.open(self.doc.source, 'r', encoding='utf-8')
            self.contents = sourcefile.read()
            sourcefile.close()
        except IOError:
            sourcefile = urllib.request.urlopen(self.doc.source)
            self.contents = sourcefile.read().decode('utf-8')
            sourcefile.close()

    def add_chunk(self, **chunk):
        if 'options' in chunk and isinstance(chunk['options'], str):
            chunk['options'] = self.parse_options(chunk['options'])
        if 'input' not in chunk:
            chunk['input'] = ''
        if 'options' not in chunk:
            chunk['options'] = {}

        self.doc.chunks.append(chunk)
        return chunk

    def add_input(self, input):
        self.doc.chunks[-1]['input'] += input

    def parse_options(self, value):
        options = {}
        for opt in value.split(','):
            parts = list(map(lambda x: x.strip(), opt.split('=')))
            if len(parts) == 1:
                options[self.default_key] = self.parse_value(parts[0])
            else:
                options[parts[0]] = self.parse_value(parts[1])

        return options

    def parse_value(self, value):
        if value == 'True':
            return True
        if value == 'False':
            return False
        return shlex.split(value)[0]

    def parse_metys(self):
        parts = re.split(r'(?s)<\|(?:\[(.*?)\])?(.*?)\|>', self.contents)
        for i in range(len(parts)):
            sub = i % 3
            if sub == 0:
                self.add_chunk(type='text', input=parts[i])
            elif sub == 1:
                self.add_chunk(type='code', input=parts[i+1], options=parts[i])

    def parse_noweb(self):
        self.add_chunk(type='text')
        parts = re.split(r'(?m)^(?:<<(.*?)>>=|@)\s*$', self.contents)
        for i in range(len(parts)):
            sub = i % 2
            if sub == 0:
                self.add_input(parts[i])
            elif parts[i]:
                self.add_chunk(type='code', options=parts[i])
            else:
                self.add_chunk(type='text')

    def parse_markdown(self):
        parts = re.split(r'(?ms)(?P<fence>^```|(?<!`)`)\{([^}]+)\}(.*?)(?P=fence)', self.contents)
        print(parts)
        for i in range(len(parts)):
            sub = i % 4
            if sub == 0:
                self.add_chunk(type='text', input=parts[i])
            elif sub == 1:
                chunk = self.add_chunk(type='code', input=parts[i+2], options=parts[i+1])
                if parts[i] == '`':
                    chunk['options']['inline'] = True

    def apply(self):
        if self.doc.options['parser'] == 'noweb':
            self.parse_noweb()
        elif self.doc.options['parser'] == 'markdown':
            self.parse_markdown()
        else:
            self.parse_metys()
