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
