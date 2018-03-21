import argparse
from Weave import Weave


ap = argparse.ArgumentParser()

ap.add_argument('input')
ap.add_argument('--format')
ap.add_argument('--kernel')
ap.add_argument('--parser')
args = ap.parse_args()

options = {}

if args.kernel is not None:
    options['kernel'] = args.kernel
if args.parser is not None:
    options['parser'] = args.parser
if args.format is not None:
    options['format'] = args.format

Weave(args.input, options)
