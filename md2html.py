# -*- coding: utf-8 -*-

# Copyright (c) 2023 Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

"""
Convert a markdown file to HTML using GitHub API.
"""

from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
import re
import argparse


def fix_refs(txt):
    def anchor(text):
        return re.sub(r"[^a-zA-Z0-9]+", "-", text.lower())

    def fix_headers(m):
        _, text = m.groups()
        # print(f"label: {label:<30}text: {text:<30}")
        return m.expand(rf'<h\1 id="{anchor(text.strip())}">\2</h\1>')

    txt = re.sub(r"<h(.)>(.*)<\/h.>", fix_headers, txt)

    def fix_refs(m):
        (
            comment,
            text,
        ) = m.groups()
        # print(f"comment: {comment:<30}text: {text:<30}")
        return m.expand(f'<a href="#{anchor(text.strip())}">{comment}«{text}»</a>')
        # return m.expand(f'<a href="#{anchor(text.strip())}">{comment}《{text}》</a>')

    txt = re.sub(r'<span class="pl-c">(.*)&lt;&lt;(.+)&gt;&gt;</span>', fix_refs, txt)

    return txt


def main(args):
    with open(args.input, "r", encoding="utf-8") as f:
        txt = f.read()

    # https://docs.github.com/es/rest/markdown
    url = "https://api.github.com/markdown"
    headers = {
        "Content-Type": "application/json",
        # "Content-Type": "text/x-markdown",
        "Accept": "application/vnd.github+json",
    }
    # Seems markdown mode is better because it generates links for headings
    body = {"text": txt, "mode": "gfm"}

    request = Request(
        url,
        json.dumps(body).encode(),
        # txt.encode(),
        headers,
        method="POST",
    )
    try:
        with (
            urlopen(request) as response,
            open(args.output, "w", encoding="utf-8") as f,
        ):
            f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
<title>{args.output}</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<!-- From: https://primer.style/css -->
<link href="https://unpkg.com/@primer/css/dist/primer.css" rel="stylesheet" />
<!-- From: https://github.com/primer/github-syntax-theme-generator -->
<!-- From: https://github.com/primer/github-syntax-light -->
<link href="https://unpkg.com/github-syntax-light/lib/github-light.css" rel="stylesheet" />
<!-- MathJax -->
<!--
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax/es5/tex-mml-chtml.js"></script>
-->
<!-- KaTeX -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{
    delimiters: [
        {{left: '$$', right: '$$', display: true}},
        {{left: '$', right: '$', display: false}},
    ],
}});"></script>
</head>
<body>
<div id="content" class="container-xl px-2 px-md-4 py-4 py-md-8 markdown-body">
{fix_refs(response.read().decode())}
</div>
</body>
</html>
    """)
    except HTTPError as e:
        print(e)
        print(e.read().decode())
        return 1
    return 0


def parse_args():
    parser = argparse.ArgumentParser(
        description="Render markdown to html using the GitHub API"
    )
    parser.add_argument("input", metavar="INPUT_FILE.md", help="Input Markdown file")
    parser.add_argument("output", metavar="OUTPUT_FILE.html", help="Output HTML file")
    return parser.parse_args()


if __name__ == "__main__":
    exit(main(parse_args()))
