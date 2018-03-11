import Processors
import argparse
from Document import Document


ap = argparse.ArgumentParser()

ap.add_argument('source')
ap.add_argument('--format')
ap.add_argument('--kernel')
ap.add_argument('--parser')
args = ap.parse_args()

doc = Document(args.source)

doc.options['kernel'] =  'python' if args.kernel == None else args.kernel

with Processors.Parse(doc) as p:
    p.apply()

with Processors.NameChunks(doc) as p:
    p.apply()

with Processors.ApplyDefaultOptions(doc) as p:
    p.apply()

with Processors.Jupyter(doc) as p:
    p.apply()

with Processors.GetResults(doc) as p:
    p.apply()

with Processors.LaTeX(doc) as p:
    p.apply()

with Processors.WriteOutput(doc) as p:
    p.apply()
