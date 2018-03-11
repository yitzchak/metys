import Processors
import argparse


ap = argparse.ArgumentParser()

ap.add_argument('source')
ap.add_argument('--format')
ap.add_argument('--kernel')
ap.add_argument('--parser')
args = ap.parse_args()

defaultOptions = {'kernel': 'python' if args.kernel == None else args.kernel}
types = [
    {'mime': 'application/pdf', 'external': True},
    {'mime': 'image/png', 'external': True},
    {'mime': 'image/jpeg', 'external': True},
    {'mime': 'text/latex', 'external': False},
    {'mime': 'text/plain', 'external': False}
]

chunks = []

with Processors.Parse(args.source) as p:
    p.apply(chunks)

with Processors.NameChunks() as p:
    p.apply(chunks)

with Processors.ApplyDefaultOptions(defaultOptions) as p:
    p.apply(chunks)

with Processors.Jupyter() as p:
    p.apply(chunks)

with Processors.GetResults(types) as p:
    p.apply(chunks)

with Processors.LaTeX() as p:
    p.apply(chunks)

with Processors.WriteOutput() as p:
    p.apply(chunks)
