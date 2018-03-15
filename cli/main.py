import Processors
import argparse
from Chunk import Chunk


ap = argparse.ArgumentParser()

ap.add_argument('source')
ap.add_argument('--format')
ap.add_argument('--kernel')
ap.add_argument('--parser')
args = ap.parse_args()

doc = Chunk(type='group', options={
    'echo': True,
    'evaluate': True,
    'inline': False,
    'results': True,
    'source': args.source,
    'name': 'doc',
    'types': [
        {'mime': 'application/pdf', 'external': True},
        {'mime': 'image/png', 'external': True},
        {'mime': 'image/jpeg', 'external': True},
        {'mime': 'text/latex', 'external': False},
        {'mime': 'text/plain', 'external': False}
    ]
})

if args.kernel != None:
    doc.options['kernel'] = args.kernel
if args.parser != None:
    doc.options['parser'] = args.parser
if args.format != None:
    doc.options['format'] = args.format

with Processors.DeduceOptions(doc) as p:
    p.apply()

with Processors.ParseInput(doc) as p:
    p.apply()

with Processors.NameChunks(doc) as p:
    p.apply()

with Processors.ApplyDefaultOptions(doc) as p:
    p.apply()

with Processors.EvaluateCode(doc) as p:
    p.apply()

with Processors.GetResults(doc) as p:
    p.apply()

with Processors.FormatOutput(doc) as p:
    p.apply()

with Processors.WriteOutput(doc) as p:
    p.apply()
