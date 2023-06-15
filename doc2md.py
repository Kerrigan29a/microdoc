
"""
Convert the documentation from the JSON format to markdown.
"""

__author__ = "Javier Escalada Gómez"
__email__ = "kerrigan29a@gmail.com"
__version__ = "0.3.0"
__license__ = "BSD 3-Clause Clear License"

from contextlib import contextmanager


def format(doc, level):
    """Format the documentation"""

    def format_node(node, level, prefix):
        """Format a node"""
        if not node["text"]:
            return
        id = f"{prefix}{node['name']}"
        yield f"{'#' * level} {node['type']} {id}\n"
        for lang, chunk in node["text"]:
            if lang:
                yield f"```{lang}\n{chunk}```\n"
            else:
                yield chunk
        yield "\n\n"
        for node in node["content"]:
            yield from format_node(node, level + 1, f"{id}.")

    def format_refs(refs):
        """Format the references"""
        yield f"<!-- references -->\n"
        for text, (destination, title) in refs.items():
            yield f'[`{text}`]: #{destination} "{title}"\n'
            yield f'[{text}]: #{destination} "{title}"\n'
    
    for node in doc["content"]:
        yield from format_node(node, level, "")
        yield "\n"
    
    yield from format_refs(collect_refs(doc))


def collect_refs(node):
    refs = {}
    for node in node["content"]:
        _collect_refs(node, refs, "")
    return refs


def _collect_refs(node, refs, prefix):
    id = f"{prefix}{node['name']}"
    refs[id] = (f"{node['type']}-{id}".replace(".", "-").lower(), f"{node['type']} {node['name']}")
    for node in node["content"]:
        _collect_refs(node, refs, f"{id}.")


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

    parser = argparse.ArgumentParser("Generate markdown documentation from JSON")
    parser.add_argument("-i", "--input", type=Path, default=None,
                        help="Input file. If not specified, the input is read from stdin")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="Output file. If not specified, the output is written to stdout")
    parser.add_argument("-s", "--start", type=int, default=1,
                        help="Start level for the headers")
    args = parser.parse_args()
    
    with reader(args.input) as r, writer(args.output) as w:
        w.writelines(format(json.load(r), args.start))
