import Processors
from Chunk import Chunk
from Formatter import LaTeXFormatter, MarkDownFormatter
import os


def Weave(options=None):
    opts = {
        'code_env': 'verbatim',
        'echo': True,
        'evaluate': True,
        'expand_options': False,
        'figure_env': 'figure',
        'figure_path': 'figure',
        'figure_prefix': 'fig:',
        'formatters': {
            'latex': LaTeXFormatter(),
            'markdown': MarkDownFormatter()
        },
        'inline': False,
        'math_env': 'equation',
        'math_prefix': 'eq:',
        'name': 'doc',
        'results': True,
        'wrap_math': True
    }

    if 'input' in options:
        dir, base = os.path.split(options['input'])
        if dir != '':
            os.chdir(dir)
            options['input'] = base

    if options is not None:
        opts.update(options)

    doc = Chunk(type='group', options=opts)

    with Processors.ParseInput(doc) as p:
        p.apply()

    with Processors.DeduceOptions(doc) as p:
        p.apply()

    with Processors.NameChunks(doc) as p:
        p.apply()

    with Processors.ApplyDefaultOptions(doc) as p:
        p.apply()

    with Processors.EvaluateCode(doc) as p:
        p.apply()

    with Processors.FormatOutput(doc) as p:
        p.apply()

    with Processors.WriteOutput(doc) as p:
        p.apply()
