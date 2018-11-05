from .Processors import *
from .Chunk import Chunk
from .Formatter import LaTeXFormatter, MarkDownFormatter
import os


def Weave(options=None):
    opts = {
        "code_echo": True,
        "code_env": "verbatim",
        "evaluate": True,
        "expand_options": False,
        "figure_env": "figure",
        "figure_path": "figure",
        "figure_prefix": "fig:",
        "formatters": {"latex": LaTeXFormatter(), "markdown": MarkDownFormatter()},
        "inline": False,
        "math_env": "equation",
        "math_prefix": "eq:",
        "math_split": True,
        "name": "doc",
        "restart": False,
        "results": True,
        "split": False,
        "stderr_echo": True,
        "stderr_env": "verbatim",
        "stdout_echo": False,
        "stdout_env": "verbatim",
        "wrap_math": True,
    }

    if options is not None:
        if "input" in options:
            dir, base = os.path.split(options["input"])
            if dir == "":
                options["root"] = "."
            else:
                options["root"] = dir
                options["input"] = base
        opts.update(options)

    doc = Chunk(type="group", options=opts)

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
