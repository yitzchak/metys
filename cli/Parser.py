import copy
import io
import re
import shlex
import urllib

class Parser(object):

    def __init__(self, source, parser=None):
        self.source = source
        self.chunks = []
        if parser:
            self.parser = parser
        elif re.search(r'(?i)\..?nw$', self.source):
            self.parser = 'noweb'
        elif re.search(r'(?i)\..?md$', self.source):
            self.parser = 'markdown'
        else:
            self.parser = 'metys'

        self.default_key = 'name' if self.parser == 'noweb' else 'kernel'

    def read(self):
        try:
            sourcefile = io.open(self.source, 'r', encoding='utf-8')
            self.content = sourcefile.read()
            sourcefile.close()
        except IOError:
            sourcefile = urllib.request.urlopen(self.source)
            self.content = sourcefile.read().decode('utf-8')
            sourcefile.close()

    def get_chunks(self):
        return copy.deepcopy(self.chunks)

    def add_chunk(self, **chunk):
        if 'options' in chunk and isinstance(chunk['options'], str):
            chunk['options'] = self.parse_options(chunk['options'])
        if 'content' not in chunk:
            chunk['content'] = ''
        if 'options' not in chunk:
            chunk['options'] = {}

        self.chunks.append(chunk)
        return chunk

    def add_content(self, content):
        self.chunks[-1]['content'] += content

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
        parts = re.split(r'(?s)<\|(\[.*?\])?(.*?)\|>', self.content)
        for i in range(len(parts)):
            sub = i % 3
            if sub == 0:
                self.add_chunk(type='text', content=parts[i])
            elif sub == 1:
                self.add_chunk(type='code', content=parts[i+1], options=parts[i])

    def parse_noweb(self):
        self.add_chunk(type='text')
        parts = re.split(r'(?m)^(?:<<(.*?)>>=|@)\s*$', self.content)
        for i in range(len(parts)):
            sub = i % 2
            if sub == 0:
                self.add_content(parts[i])
            elif parts[i]:
                self.add_chunk(type='code', options=parts[i])
            else:
                self.add_chunk(type='text')

    def parse_markdown(self):
        parts = re.split(r'(?ms)(?P<fence>^```|(?<!`)`)\{([^}]+)\}(.*?)(?P=fence)', self.content)
        print(parts)
        for i in range(len(parts)):
            sub = i % 4
            if sub == 0:
                self.add_chunk(type='text', content=parts[i])
            elif sub == 1:
                chunk = self.add_chunk(type='code', content=parts[i+2], options=parts[i+1])
                if parts[i] == '`':
                    chunk['options']['inline'] = True

    def parse(self):
        self.read()

        if self.parser == 'noweb':
            self.parse_noweb()
        elif self.parser == 'markdown':
            self.parse_markdown()
        else:
            self.parse_metys()
