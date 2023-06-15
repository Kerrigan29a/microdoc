
"""
Convert the documentation from the JSON format to markdown.
"""

__author__ = "Javier Escalada Gómez"
__email__ = "kerrigan29a@gmail.com"
__version__ = "0.2.0"
__license__ = "BSD 3-Clause Clear License"

from contextlib import contextmanager


def format(doc):
    """ Compose the markdown document from the documentation tree structure.

    It just copy verbatim the text chunks, and add a header for each node.
    There are two exceptions:
    * Any text chunk associated to a programming language is enclosed in a code block.
    """
    yield from _format(doc["doc"], 1)
    yield "\n\n"
    for text, (destination, title) in collect_refs(doc["doc"]).items():
        yield f'[`{text}`]: #{destination} "{title}"\n'
        yield f'[{text}]: #{destination} "{title}"\n'


def _format(node, level):
    if not node["text"]:
        return
    yield f"{'#' * level} {node['type']} `{node['name']}`\n"
    for lang, chunk in node["text"]:
        if lang:
            yield f"```{lang}\n{chunk}```\n"
        else:
            yield chunk
    yield "\n\n"
    for node in node["content"]:
        yield from _format(node, level + 1)


def collect_refs(doc):
    """ Collect all the symbols that can be referenced in the documentation.
    
    A symbol can be referenced if it has an entry in the documentation.
    """
    refs = {}
    _collect_refs(doc, refs)
    return refs


def _collect_refs(node, refs):
    if node["text"]:
        refs[node["name"]] = (f"{node['type']}-{node['name']}".lower(), f"{node['type']} {node['name']}")
    for node in node["content"]:
        _collect_refs(node, refs)


@contextmanager
def reader(input):
    if input is None:
        yield sys.stdin
    else:
        with input.open("r") as f:
            yield f


@contextmanager
def writer(output):
    if output is None:
        yield sys.stdout
    else:
        with output.open("w") as f:
            yield f


if __name__ == "__main__":
    import sys
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser("Format documentation as markdown")
    parser.add_argument("-i", "--input", type=Path, default=None)
    parser.add_argument("-o", "--output", type=Path, default=None)
    args = parser.parse_args()
    
    with reader(args.input) as r, writer(args.output) as w:
        w.writelines(format(json.load(r)))