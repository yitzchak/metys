import argparse
from .Weave import Weave

def main():
    ap = argparse.ArgumentParser(prog='metys')

    ap.add_argument("input", help="Path of input file.")

    g = ap.add_mutually_exclusive_group()
    g.add_argument(
        "--code-echo",
        dest="code_echo",
        action="store_true",
        help="Enable echo of code input.",
    )
    g.add_argument(
        "--no-code-echo",
        dest="code_echo",
        action="store_false",
        help="Disable echo of code input.",
    )

    ap.add_argument("--code-env", help="Default code environment for LaTeX.")

    ap.add_argument(
        "--code-env-options", help="Default code environment options for LaTeX."
    )

    g = ap.add_mutually_exclusive_group()
    g.add_argument(
        "--evaluate",
        dest="evaluate",
        action="store_true",
        help="Enable evaluation of code input.",
    )
    g.add_argument(
        "--no-evaluate",
        dest="evaluate",
        action="store_false",
        help="Disable evaluation of code input.",
    )

    g = ap.add_mutually_exclusive_group()
    g.add_argument(
        "--expand-options",
        dest="expand_options",
        action="store_true",
        help="Enable option expansion in code input.",
    )
    g.add_argument(
        "--no-expand-options",
        dest="expand_options",
        action="store_false",
        help="Disable option expansion in code input.",
    )

    ap.add_argument("--figure-env", help="Default figure environment for LaTeX.")

    ap.add_argument("--figure-path", help="Default figure directory.")

    ap.add_argument(
        "--figure-env-options", help="Default figure environment options for LaTeX."
    )

    ap.add_argument("--figure-prefix", help="Default figure label prefix for LaTeX.")

    ap.add_argument(
        "--format", choices=["latex", "markdown"], help="Format of output file."
    )

    ap.add_argument("--graphics-options", help="Default graphics options for LaTeX.")

    ap.add_argument("--kernel", help="Default Jupyter kernel.")

    ap.add_argument("--math-env", help="Default display math environment for LaTeX.")

    ap.add_argument("--math-prefix", help="Default mathematics label prefix for LaTeX.")

    ap.add_argument("--output", help="Path of desplay file.")

    ap.add_argument(
        "--parser",
        choices=["markdown", "metys", "noweb"],
        help="Parser to use for input file.",
    )

    g = ap.add_mutually_exclusive_group()
    g.add_argument(
        "--results",
        dest="results",
        action="store_true",
        help="Enable output of code results.",
    )
    g.add_argument(
        "--no-results",
        dest="results",
        action="store_false",
        help="Disable output of code results.",
    )

    g = ap.add_mutually_exclusive_group()
    g.add_argument(
        "--stderr-echo",
        dest="stderr_echo",
        action="store_true",
        help="Enable echo of stderr.",
    )
    g.add_argument(
        "--no-stderr-echo",
        dest="stderr_echo",
        action="store_false",
        help="Disable echo of stderr.",
    )

    ap.add_argument("--stderr-env", help="Default stderr environment for LaTeX.")

    ap.add_argument(
        "--stderr-env-options", help="Default stderr environment options for LaTeX."
    )

    g = ap.add_mutually_exclusive_group()
    g.add_argument(
        "--stdout-echo",
        dest="stdout_echo",
        action="store_true",
        help="Enable echo of stdout.",
    )
    g.add_argument(
        "--no-stdout-echo",
        dest="stdout_echo",
        action="store_false",
        help="Disable echo of stdout.",
    )

    ap.add_argument("--stdout-env", help="Default stdout environment for LaTeX.")

    ap.add_argument(
        "--stdout-env-options", help="Default stdout environment options for LaTeX."
    )

    g = ap.add_mutually_exclusive_group()
    g.add_argument(
        "--wrap-math",
        dest="wrap_math",
        action="store_true",
        help="Enabling wrapping of math results in appropriate format environment.",
    )
    g.add_argument(
        "--no-wrap-math",
        dest="wrap_math",
        action="store_false",
        help="Disable wrapping of math results in appropriate format environment.",
    )

    ap.set_defaults(
        code_echo=None,
        evaluate=None,
        expand_options=None,
        results=None,
        stdout_echo=None,
        stderr_echo=None,
        wrap_math=None,
    )

    args = ap.parse_args()

    options = {k: v for k, v in vars(args).items() if v is not None}

    Weave(options)


if __name__ == "__main__":
    main()
