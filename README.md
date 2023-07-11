# μdoc - A minimalistic documentation generator

This is just a set of scripts to generate documentation from any programming language.
The idea is to divide the process into two steps:

1. Extract the documentation from the source code and save it to a JSON file.
   The scripts implementing this part should be named `x2doc`, where `x` is the programming language.
   At the moment, only `py2doc` is implemented.

2. Format the documentation in Markdown. The script implementing this part is `doc2md`.
   It just copies verbatim the documentation from the JSON file to the Markdown file.
   The only exceptions to this rule are the following ones:

   * Every element in the JSON file is a section of the Markdown file. The script formats the heading.

   * When a text chunk is marked as code, the script formats it as a [fenced code block](https://www.markdownguide.org/extended-syntax/#fenced-code-blocks) with [syntax highlighting](https://www.markdownguide.org/extended-syntax/#syntax-highlighting).

   * For each generated Markdown file, the script injects all known [link destinations](https://spec.commonmark.org/0.30/#link-destination) at the end of the file.
   
   Any additional formatting should be done in the documentation itself.

## Module [py2doc](https://github.com/kerrigan29a/microdoc/blob/main/py2doc.py#L1)
Extract the docstrings from a Python file and store them in a JSON file.
This script doesn't care about the format of the docstrings, it just extracts
them. The only exception to this rule is when it finds a doctest, in which case
it labels this code snippet as Python code.

```
usage: py2doc.py [-h] [-o OUTPUT] [-e ENCODING]
                 INPUT[:NAME] [INPUT[:NAME] ...]

Extract docstrings from Python

positional arguments:
  INPUT[:NAME]          Input file. If the input is followed by a colon, the
                        text before the colon is used as the module name

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file. If not specified, the output is written
                        to stdout
  -e ENCODING, --encoding ENCODING
                        Encoding of the input files

```
### Function [py2doc.process_node](https://github.com/kerrigan29a/microdoc/blob/main/py2doc.py#L29)
```python
def process_node(node, path): ...
```
Extract the information from an AST node.

If the docstring contains doctests, the docstring is split into chunks.
The doctests are labeled as Python code, and the rest of the docstring is labeled as text.

### Function [py2doc._compose_definition](https://github.com/kerrigan29a/microdoc/blob/main/py2doc.py#L84)
```python
def _compose_definition(code): ...
```
Compose the definition of a function or method from its code.

```python
>>> _compose_definition("def foo(a, b): return a + b")
'def foo(a, b): ...'
>>> _compose_definition("async def foo(a, b): return a + b")
'async def foo(a, b): ...'
>>> _compose_definition("def foo(a : int, b : int) -> int: return a + b")
'def foo(a : int, b : int) -> int: ...'
```


### Function [py2doc.writer](https://github.com/kerrigan29a/microdoc/blob/main/py2doc.py#L100)
```python
@contextmanager
def writer(output): ...
```
Open a file for writing or use stdout if the output is None. 


## Module [doc2md](https://github.com/kerrigan29a/microdoc/blob/main/doc2md.py#L1)
Format the documentation from JSON to markdown.

```
usage: doc2md.py [-h] [-i INPUT] [-o OUTPUT] [-l LEVEL] [-u URL]

Generate markdown documentation from JSON

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file. If not specified, the input is read from
                        stdin
  -o OUTPUT, --output OUTPUT
                        Output file. If not specified, the output is written
                        to stdout
  -l LEVEL, --level LEVEL
                        Start level for the headers
  -u URL, --url URL     URL template for the links

```
### Function [doc2md.format](https://github.com/kerrigan29a/microdoc/blob/main/doc2md.py#L16)
```python
def format(doc, level, url=None): ...
```
Format the documentation.

#### Function [doc2md.format.format_node](https://github.com/kerrigan29a/microdoc/blob/main/doc2md.py#L19)
```python
def format_node(node, level, prefix): ...
```
Format a node. 

#### Function [doc2md.format.format_refs](https://github.com/kerrigan29a/microdoc/blob/main/doc2md.py#L40)
```python
def format_refs(refs): ...
```
Format the references.

It generates two destination link for every element in the JSON file.
One with the text as the destination, and another with the text surrounded by backticks.

### Function [doc2md.collect_refs](https://github.com/kerrigan29a/microdoc/blob/main/doc2md.py#L58)
```python
def collect_refs(node): ...
```
Collect the references from the JSON file.

To compose the link, it uses the standard GitHub approach:
1. Start with the header text.
2. Convert all letters to lowercase.
3. Replace all spaces and non-alphanumeric characters with hyphens.    

### Function [doc2md.reader](https://github.com/kerrigan29a/microdoc/blob/main/doc2md.py#L81)
```python
@contextmanager
def reader(input): ...
```
Open the input file, or stdin if not specified. 

### Function [doc2md.writer](https://github.com/kerrigan29a/microdoc/blob/main/doc2md.py#L91)
```python
@contextmanager
def writer(output): ...
```
Open the output file, or stdout if not specified. 


<!-- references -->
[py2doc]: #module-py2doc "Module py2doc"
[`py2doc`]: #module-py2doc "Module py2doc"
[py2doc.process_node]: #function-py2doc-process_node "Function process_node"
[`py2doc.process_node`]: #function-py2doc-process_node "Function process_node"
[py2doc._compose_definition]: #function-py2doc-_compose_definition "Function _compose_definition"
[`py2doc._compose_definition`]: #function-py2doc-_compose_definition "Function _compose_definition"
[py2doc.writer]: #function-py2doc-writer "Function writer"
[`py2doc.writer`]: #function-py2doc-writer "Function writer"
[doc2md]: #module-doc2md "Module doc2md"
[`doc2md`]: #module-doc2md "Module doc2md"
[doc2md.format]: #function-doc2md-format "Function format"
[`doc2md.format`]: #function-doc2md-format "Function format"
[doc2md.format.format_node]: #function-doc2md-format-format_node "Function format_node"
[`doc2md.format.format_node`]: #function-doc2md-format-format_node "Function format_node"
[doc2md.format.format_refs]: #function-doc2md-format-format_refs "Function format_refs"
[`doc2md.format.format_refs`]: #function-doc2md-format-format_refs "Function format_refs"
[doc2md.collect_refs]: #function-doc2md-collect_refs "Function collect_refs"
[`doc2md.collect_refs`]: #function-doc2md-collect_refs "Function collect_refs"
[doc2md.collect_refs.collect]: #function-doc2md-collect_refs-collect "Function collect"
[`doc2md.collect_refs.collect`]: #function-doc2md-collect_refs-collect "Function collect"
[doc2md.reader]: #function-doc2md-reader "Function reader"
[`doc2md.reader`]: #function-doc2md-reader "Function reader"
[doc2md.writer]: #function-doc2md-writer "Function writer"
[`doc2md.writer`]: #function-doc2md-writer "Function writer"
