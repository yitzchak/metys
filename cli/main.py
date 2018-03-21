import argparse
from Weave import Weave


ap = argparse.ArgumentParser()

ap.add_argument('input', help='Path of input file.')

ap.add_argument('--code-env', help='Default code environment for LaTeX.')

ap.add_argument('--code-env-options', help='Default code environment options for LaTeX.')

g = ap.add_mutually_exclusive_group()
g.add_argument('--echo', dest='echo', action='store_true',
               help='Enable echo of code input.')
g.add_argument('--no-echo', dest='echo', action='store_false',
               help='Disable echo of code input.')

g = ap.add_mutually_exclusive_group()
g.add_argument('--evaluate', dest='evaluate', action='store_true',
               help='Enable evaluation of code input.')
g.add_argument('--no-evaluate', dest='evaluate', action='store_false',
               help='Disable evaluation of code input.')

g = ap.add_mutually_exclusive_group()
g.add_argument('--expand-options', dest='expand_options', action='store_true',
               help='Enable option expansion in code input.')
g.add_argument('--no-expand-options', dest='expand_options', action='store_false',
               help='Disable option expansion in code input.')

ap.add_argument('--figure-env', help='Default figure environment for LaTeX.')

ap.add_argument('--figure-path', help='Default figure directory.')

ap.add_argument('--figure-pos', help='Default figure postion for LaTeX.')

ap.add_argument('--figure-prefix', help='Default figure label prefix for LaTeX.')

ap.add_argument('--format', choices=['latex', 'markdown'],
                help='Format of output file.')

ap.add_argument('--kernel', help='Default Jupyter kernel.')

ap.add_argument('--math-env', help='Default display math environment for LaTeX.')

ap.add_argument('--math-prefix', help='Default mathematics label prefix for LaTeX.')

ap.add_argument('--output', help='Path of desplay file.')

ap.add_argument('--parser', choices=['markdown', 'metys', 'noweb'],
                help='Parser to use for input file.')

g = ap.add_mutually_exclusive_group()
g.add_argument('--results', dest='results', action='store_true',
               help='Enable output of code results.')
g.add_argument('--no-results', dest='results', action='store_false',
               help='Disable output of code results.')

g = ap.add_mutually_exclusive_group()
g.add_argument('--wrap-math', dest='wrap_math', action='store_true',
               help='Enabling wrapping of math results in appropriate format environment.')
g.add_argument('--no-wrap-math', dest='wrap_math', action='store_false',
               help='Disable wrapping of math results in appropriate format environment.')

ap.set_defaults(echo=None, evaluate=None, expand_options=None, results=None,
                wrap_math=None)

args = ap.parse_args()

options = {k: v for k, v in vars(args).items() if v is not None}

Weave(options)
