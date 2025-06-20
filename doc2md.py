# -*- coding: utf-8 -*-

# Copyright (c) 2023 Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

"""
Format the documentation from JSON to markdown.
"""

__author__ = "Javier Escalada Gómez"
__email__ = "kerrigan29a@gmail.com"
__version__ = "0.5.1"
__license__ = "BSD 3-Clause Clear License"

from contextlib import contextmanager
import sys


def format(doc, level, url=None):
    """Format the documentation."""

    def format_node(node, level, prefix):
        """Format a node."""
        nonlocal url
        if not node["text"]:
            return
        header = f"{'#' * level} {node['type']}"
        id = f"{prefix}{escape_markdown(node['name'])}"
        if url:
            path, line = node["location"]
            yield f"{header} [{id}]({url.format(path=path, line=line)})\n"
        else:
            yield f"{header} {id}\n"
        yield node["text"]
        yield "\n\n"
        for node in node["content"]:
            yield from format_node(node, level + 1, f"{id}.")

    def format_refs(refs):
        """Format the references.

        It generates two destination link for every element in the JSON file.
        One with the text as the destination, and another with the text surrounded by backticks.
        """
        yield "<!-- references -->\n"
        for text, (destination, title) in refs.items():
            yield f'[{text}]: #{destination} "{title}"\n'
            yield f'[`{text}`]: #{destination} "{title}"\n'

    for node in doc["content"]:
        yield from format_node(node, level, "")
        yield "\n"

    yield from format_refs(collect_refs(doc))


def escape_markdown(text):
    """Escape the markdown characters."""
    return text.replace("_", "\\_").replace("*", "\\*").replace("`", "\\`")


def collect_refs(node):
    """
    Collect the references from the JSON file.

    To compose the link, it uses the standard GitHub approach:
    1. Start with the header text.
    2. Convert all letters to lowercase.
    3. Replace all spaces and non-alphanumeric characters with hyphens.
    """

    def collect(node, refs, prefix):
        id = f"{prefix}{node['name']}"
        refs[id] = (
            f"{node['type']}-{id}".replace(".", "-").lower(),
            f"{node['type']} {node['name']}",
        )
        for node in node["content"]:
            collect(node, refs, f"{id}.")

    refs = {}
    for node in node["content"]:
        collect(node, refs, "")
    return refs


@contextmanager
def reader(input):
    """Open the input file, or stdin if not specified."""
    if input is None:
        yield sys.stdin
    else:
        with input.open("r") as f:
            yield f


@contextmanager
def writer(output):
    """Open the output file, or stdout if not specified."""
    if output is None:
        yield sys.stdout
    else:
        with output.open("w") as f:
            yield f


def parse_args(argv=None):
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="Generate markdown documentation from JSON"
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=None,
        help="Input file. If not specified, the input is read from stdin",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file. If not specified, the output is written to stdout",
    )
    parser.add_argument(
        "-l",
        "--level",
        type=int,
        default=1,
        help="Start level for the headers",
    )
    parser.add_argument("-u", "--url", default=None, help="URL template for the links")
    return parser.parse_args(argv)


def main(argv=None):
    import json

    args = parse_args(argv)
    with reader(args.input) as r, writer(args.output) as w:
        w.writelines(format(json.load(r), args.level, args.url))


if __name__ == "__main__":
    raise SystemExit(main())
