"""
Extract the docstrings from a Python file and store them in a JSON file.
This script does't care the format of the docstrings, it just extract them.
The only exception to this rule is when it finds a doctest, in which case it
labels this code snippet as Python code.

{{PY2DOC_USAGE}}
"""

__author__ = "Javier Escalada Gómez"
__email__ = "kerrigan29a@gmail.com"
__version__ = "0.3.0"
__license__ = "BSD 3-Clause Clear License"

import ast
import sys
from contextlib import contextmanager
from doctest import DocTestParser, Example


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
        parser = DocTestParser()

        chunks1 = []
        for chunk in parser.parse(text):
            if chunk == "":
                continue
            if isinstance(chunk, Example):
                source = ">>> " + chunk.source.rstrip().replace("\n", "\n... ")
                chunks1.append(["python", f"{source}\n{chunk.want}"])
            else:
                chunks1.append([None, chunk])
        if len(chunks1) == 0:
            raise ValueError("No chunks")
        elif len(chunks1) == 1:
            text = chunks1
        else:
            last = chunks1[0]
            chunks2 = []
            for chunk in chunks1[1:]:
                if chunk[0] == last[0]:
                    last[1] += chunk[1]
                else:
                    chunks2.append(last)
                    last = chunk
            if last != chunks2[-1]:
                chunks2.append(last)
            text = chunks2

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            definition = ast.unparse(node)
            stop = definition.index(":")
            definition = definition[:stop+1].rstrip()
            definition += " ...\n"
            text.insert(0, ["python", definition])
            
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


@contextmanager
def writer(output):
    """ Open a file for writing or use stdout if the output is None.

    >>> with writer(None) as f:
    ...     f == sys.stdout
    True
    >>> import tempfile
    >>> tmp = tempfile.NamedTemporaryFile()
    >>> with writer(tmp.name) as f:
    ...     f != sys.stdout
    True
    >>> tmp.close()
    """
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
            doc["content"].append(node)

    with writer(args.output) as f:
        json.dump(doc, f, indent=4)
