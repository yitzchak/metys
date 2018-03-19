import Processors
import argparse
from Chunk import Chunk
import os


ap = argparse.ArgumentParser()

ap.add_argument('input')
ap.add_argument('--format')
ap.add_argument('--kernel')
ap.add_argument('--parser')
args = ap.parse_args()

dir, input = os.path.split(args.input)
os.chdir(dir)

doc = Chunk(type='group', options={
    'echo': True,
    'evaluate': True,
    'inline': False,
    'results': True,
    'input': input,
    'name': 'doc',
    'mimetypes': [
        'application/pdf',
        'image/png',
        'image/jpeg',
        'text/latex',
        'text/plain'
    ],
    'math_env': 'equation',
    'figure_env': 'figure',
    'code_env': 'verbatim'
})

if args.kernel is not None:
    doc.options['kernel'] = args.kernel
if args.parser is not None:
    doc.options['parser'] = args.parser
if args.format is not None:
    doc.options['format'] = args.format

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
