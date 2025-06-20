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
   * For each generated Markdown file, the script injects all known [link destinations](https://spec.commonmark.org/0.30/#link-destination) at the end of the file.
   
   Any additional formatting should be done in the documentation itself.

# Command line usage

## py2doc

```
usage: py2doc.py [-h] [-o OUTPUT] [-e ENCODING]
                 INPUT[:NAME] [INPUT[:NAME] ...]

Extract docstrings from Python

positional arguments:
  INPUT[:NAME]          Input file. If the input is followed by a colon, the
                        text before the colon is used as the module name

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Output file. If not specified, the output is written
                        to stdout
  -e, --encoding ENCODING
                        Encoding of the input files
```

## doc2md

```
usage: doc2md.py [-h] [-i INPUT] [-o OUTPUT] [-l LEVEL] [-u URL]

Generate markdown documentation from JSON

options:
  -h, --help           show this help message and exit
  -i, --input INPUT    Input file. If not specified, the input is read from
                       stdin
  -o, --output OUTPUT  Output file. If not specified, the output is written to
                       stdout
  -l, --level LEVEL    Start level for the headers
  -u, --url URL        URL template for the links
```

## md2html

```
usage: md2html.py [-h] INPUT_FILE.md OUTPUT_FILE.html

Render markdown to html using the GitHub API

positional arguments:
  INPUT_FILE.md     Input Markdown file
  OUTPUT_FILE.html  Output HTML file

options:
  -h, --help        show this help message and exit
```

# What is `doctest_utils.py` for?

At this moment, [doctest.testmod](https://docs.python.org/3/library/doctest.html#doctest.testmod)
does not allow to specify a custom [doctesr.DocTestParser](https://docs.python.org/3/library/doctest.html#doctest.DocTestParser).
This is a problem if you want to wrap a doctest example with a [fenced code block](https://spec.commonmark.org/0.30/#fenced-code-blocks).

~~~python
import doctest

def sum(a, b):
   """ This function sums two numbers.

   ```python
   >>> sum(1, 2)
   3
   ```
   """
   return a + b

result = doctest.testmod()
exit(int(bool(result.failed)))
~~~

```
**********************************************************************
File "__main__", line 8, in __main__.sum
Failed example:
    sum(1, 2)
Expected:
    3
    ```
Got:
    3
**********************************************************************
1 items had failures:
   1 of   1 in __main__.sum
***Test Failed*** 1 failures.
```

To solve this problem, you can use [doctest_utils.MarkdownDocTestParser] through [doctest_utils.testmod].

~~~python
import doctest
import doctest_utils

def sum(a, b):
   """ This function sums two numbers.

   ```python
   >>> sum(1, 2)
   3
   ```
   """
   return a + b

parser = doctest_utils.MarkdownDocTestParser()
result = doctest_utils.testmod(parser=parser)
exit(int(bool(result.failed)))
~~~

# Documentation
## Module [\_\_init\_\_](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/__init__.py#L1)
Microdoc package exposing the command line tools.



## Module [doc2md](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/doc2md.py#L1)
Format the documentation from JSON to markdown.

### Function [doc2md.format](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/doc2md.py#L17)
```python
def format(doc, level, url=None): ...
```
Format the documentation.

#### Function [doc2md.format.format\_node](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/doc2md.py#L20)
```python
def format_node(node, level, prefix): ...
```
Format a node.

#### Function [doc2md.format.format\_refs](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/doc2md.py#L37)
```python
def format_refs(refs): ...
```
Format the references.

It generates two destination link for every element in the JSON file.
One with the text as the destination, and another with the text surrounded by backticks.

### Function [doc2md.escape\_markdown](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/doc2md.py#L55)
```python
def escape_markdown(text): ...
```
Escape the markdown characters.

### Function [doc2md.collect\_refs](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/doc2md.py#L60)
```python
def collect_refs(node): ...
```
Collect the references from the JSON file.

To compose the link, it uses the standard GitHub approach:
1. Start with the header text.
2. Convert all letters to lowercase.
3. Replace all spaces and non-alphanumeric characters with hyphens.

### Function [doc2md.reader](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/doc2md.py#L86)
```python
@contextmanager
def reader(input): ...
```
Open the input file, or stdin if not specified.

### Function [doc2md.writer](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/doc2md.py#L96)
```python
@contextmanager
def writer(output): ...
```
Open the output file, or stdout if not specified.


## Module [doctest\_utils](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/doctest_utils.py#L1)
Extension of [doctest](https://docs.python.org/3/library/doctest.html) to allow
testing Markdown texts.

### Class [doctest\_utils.MarkdownDocTestParser](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/doctest_utils.py#L26)
A [doctest.DocTestParser](https://docs.python.org/3/library/doctest.html#doctest.DocTestParser)
that allows use Markdown fences as [doctest](https://docs.python.org/3/library/doctest.html) examples.

This class just patches the original DocTestParser._EXAMPLE_RE to exclude
Markdown fences (```` ``` ```` or `~~~`) from the WANT group.

**NOTE**: This is much better that just removing the fences from the source.
Removing lines from the source will make useless the line numbers in the
traceback.

### Function [doctest\_utils.testmod](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/doctest_utils.py#L56)
```python
def testmod(m=None, name=None, globs=None, verbose=None, report=True, optionflags=0, extraglobs=None, raise_on_error=False, exclude_empty=False, parser=DocTestParser()): ...
```
Same as [doctest.testmod](https://docs.python.org/3/library/doctest.html#doctest.testmod)
but allows to specify a custom DocTestParser.

All `master` related code is removed.



## Module [md2html](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/md2html.py#L1)
Convert a markdown file to HTML using GitHub API.


## Module [py2doc](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/py2doc.py#L1)
Extract the docstrings from a Python file and store them in a JSON file.
This script doesn't care about the format of the docstrings, it just extracts
them. The only exception to this rule is when it finds a doctest, in which case
it labels this code snippet as Python code.

### Function [py2doc.process\_node](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/py2doc.py#L29)
```python
def process_node(node, path): ...
```
Extract the information from an AST node.

If the docstring contains doctests, the docstring is split into chunks.
The doctests are labeled as Python code, and the rest of the docstring is labeled as text.

### Function [py2doc.\_compose\_definition](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/py2doc.py#L56)
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

### Function [py2doc.writer](https://github.com/kerrigan29a/microdoc/blob/main/microdoc/py2doc.py#L74)
```python
@contextmanager
def writer(output): ...
```
Open a file for writing or use stdout if the output is None.


<!-- references -->
[__init__]: #module-__init__ "Module __init__"
[`__init__`]: #module-__init__ "Module __init__"
[_version]: #module-_version "Module _version"
[`_version`]: #module-_version "Module _version"
[doc2md]: #module-doc2md "Module doc2md"
[`doc2md`]: #module-doc2md "Module doc2md"
[doc2md.format]: #function-doc2md-format "Function format"
[`doc2md.format`]: #function-doc2md-format "Function format"
[doc2md.format.format_node]: #function-doc2md-format-format_node "Function format_node"
[`doc2md.format.format_node`]: #function-doc2md-format-format_node "Function format_node"
[doc2md.format.format_refs]: #function-doc2md-format-format_refs "Function format_refs"
[`doc2md.format.format_refs`]: #function-doc2md-format-format_refs "Function format_refs"
[doc2md.escape_markdown]: #function-doc2md-escape_markdown "Function escape_markdown"
[`doc2md.escape_markdown`]: #function-doc2md-escape_markdown "Function escape_markdown"
[doc2md.collect_refs]: #function-doc2md-collect_refs "Function collect_refs"
[`doc2md.collect_refs`]: #function-doc2md-collect_refs "Function collect_refs"
[doc2md.collect_refs.collect]: #function-doc2md-collect_refs-collect "Function collect"
[`doc2md.collect_refs.collect`]: #function-doc2md-collect_refs-collect "Function collect"
[doc2md.reader]: #function-doc2md-reader "Function reader"
[`doc2md.reader`]: #function-doc2md-reader "Function reader"
[doc2md.writer]: #function-doc2md-writer "Function writer"
[`doc2md.writer`]: #function-doc2md-writer "Function writer"
[doctest_utils]: #module-doctest_utils "Module doctest_utils"
[`doctest_utils`]: #module-doctest_utils "Module doctest_utils"
[doctest_utils.MarkdownDocTestParser]: #class-doctest_utils-markdowndoctestparser "Class MarkdownDocTestParser"
[`doctest_utils.MarkdownDocTestParser`]: #class-doctest_utils-markdowndoctestparser "Class MarkdownDocTestParser"
[doctest_utils.testmod]: #function-doctest_utils-testmod "Function testmod"
[`doctest_utils.testmod`]: #function-doctest_utils-testmod "Function testmod"
[inject_usage]: #module-inject_usage "Module inject_usage"
[`inject_usage`]: #module-inject_usage "Module inject_usage"
[md2html]: #module-md2html "Module md2html"
[`md2html`]: #module-md2html "Module md2html"
[md2html.fix_refs]: #function-md2html-fix_refs "Function fix_refs"
[`md2html.fix_refs`]: #function-md2html-fix_refs "Function fix_refs"
[md2html.fix_refs.anchor]: #function-md2html-fix_refs-anchor "Function anchor"
[`md2html.fix_refs.anchor`]: #function-md2html-fix_refs-anchor "Function anchor"
[md2html.fix_refs.fix_headers]: #function-md2html-fix_refs-fix_headers "Function fix_headers"
[`md2html.fix_refs.fix_headers`]: #function-md2html-fix_refs-fix_headers "Function fix_headers"
[md2html.fix_refs.fix_refs]: #function-md2html-fix_refs-fix_refs "Function fix_refs"
[`md2html.fix_refs.fix_refs`]: #function-md2html-fix_refs-fix_refs "Function fix_refs"
[md2html.main]: #function-md2html-main "Function main"
[`md2html.main`]: #function-md2html-main "Function main"
[md2html.parse_args]: #function-md2html-parse_args "Function parse_args"
[`md2html.parse_args`]: #function-md2html-parse_args "Function parse_args"
[py2doc]: #module-py2doc "Module py2doc"
[`py2doc`]: #module-py2doc "Module py2doc"
[py2doc.process_node]: #function-py2doc-process_node "Function process_node"
[`py2doc.process_node`]: #function-py2doc-process_node "Function process_node"
[py2doc._compose_definition]: #function-py2doc-_compose_definition "Function _compose_definition"
[`py2doc._compose_definition`]: #function-py2doc-_compose_definition "Function _compose_definition"
[py2doc.writer]: #function-py2doc-writer "Function writer"
[`py2doc.writer`]: #function-py2doc-writer "Function writer"
