from Parser import Parser
import Processors
import argparse


ap = argparse.ArgumentParser()

ap.add_argument('source')
ap.add_argument('--kernel')
args = ap.parse_args()

p = Parser(args.source)
p.parse()
chunks = p.get_chunks()

a=Processors.ApplyDefaultOptions({'kernel': 'python' if args.kernel == None else args.kernel})
a.apply(chunks)

with Processors.Jupyter() as j:
    j.apply(chunks)

print(chunks)
