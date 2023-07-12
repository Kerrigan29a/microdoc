# -*- coding: utf-8 -*-

# Copyright (c) 2023 Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

"""
Extract the docstrings from a Python file and store them in a JSON file.
This script doesn't care about the format of the docstrings, it just extracts
them. The only exception to this rule is when it finds a doctest, in which case
it labels this code snippet as Python code.
"""

__author__ = "Javier Escalada Gómez"
__email__ = "kerrigan29a@gmail.com"
__version__ = "0.5.0"
__license__ = "BSD 3-Clause Clear License"

import ast
import sys
from contextlib import contextmanager


NODE_TYPES = {
    ast.Module: "Module",
    ast.ClassDef: "Class",
    ast.FunctionDef: "Function",
    ast.AsyncFunctionDef: "Function",
}


def process_node(node, path):
    """ Extract the information from an AST node.

    If the docstring contains doctests, the docstring is split into chunks.
    The doctests are labeled as Python code, and the rest of the docstring is labeled as text.
    """
    node_type = NODE_TYPES.get(type(node))
    text = ast.get_docstring(node)
    line = getattr(node, "lineno", 1)

    if text is not None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            text = f"```python\n{_compose_definition(ast.unparse(node))}\n```\n" + text
            
    children = [
        process_node(n, path) for n in node.body if isinstance(n, tuple(NODE_TYPES))
    ]

    return {
        "type": node_type,
        "name": getattr(node, "name", None),
        "location": [path.as_posix(), line],
        "text": text,
        "content": children,
    }


def _compose_definition(code):
    """ Compose the definition of a function or method from its code.
    
    ```python
    >>> _compose_definition("def foo(a, b): return a + b")
    'def foo(a, b): ...'
    >>> _compose_definition("async def foo(a, b): return a + b")
    'async def foo(a, b): ...'
    >>> _compose_definition("def foo(a : int, b : int) -> int: return a + b")
    'def foo(a : int, b : int) -> int: ...'
    ```
    """
    min = code.index(")")
    stop = code[min:].index(":") + min
    return code[:stop+1].rstrip() + " ..."


@contextmanager
def writer(output):
    """ Open a file for writing or use stdout if the output is None. """
    if output is None:
        yield sys.stdout
    else:
        with open(output, "w", encoding="utf-8") as f:
            yield f


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path
    

    parser = argparse.ArgumentParser(description="Extract docstrings from Python")
    parser.add_argument("inputs", metavar="INPUT[:NAME]", nargs="+",
                        help="Input file. If the input is followed by a colon, the text before the colon is used as the module name")
    parser.add_argument("-o", "--output", default=None,
                        help="Output file. If not specified, the output is written to stdout")
    parser.add_argument("-e", "--encoding", default="utf-8",
                        help="Encoding of the input files")
    args = parser.parse_args()

    doc = {
        "version": __version__,
        "content": [],
    }
    for input in args.inputs:
        if ":" in input:
            input, module_name = input.split(":", 1)
            input = Path(input)
        else:
            input = Path(input)
            module_name = input.stem
        with open(input, "r", encoding=args.encoding) as f:
            node = process_node(ast.parse(f.read()), input)
            node["name"] = module_name
            doc["content"].append(node) # type: ignore

    with writer(args.output) as f:
        json.dump(doc, f, indent=4)
