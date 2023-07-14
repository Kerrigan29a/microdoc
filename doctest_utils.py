# -*- coding: utf-8 -*-

# Copyright (c) 2023 Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

"""
Extension of [doctest](https://docs.python.org/3/library/doctest.html) to allow
testing Markdown texts.
"""

__author__ = "Javier Escalada Gómez"
__email__ = "kerrigan29a@gmail.com"
__version__ = "0.2.0"
__license__ = "BSD 3-Clause Clear License"

from doctest import DocTestFinder, DocTestParser, DebugRunner, DocTestRunner, TestResults
import inspect
import re
import sys


class MarkdownDocTestParser(DocTestParser):
    """A [doctest.DocTestParser](https://docs.python.org/3/library/doctest.html#doctest.DocTestParser)
    that allows use Markdown fences as [doctest](https://docs.python.org/3/library/doctest.html) examples.

    This class just patches the original DocTestParser._EXAMPLE_RE to exclude
    Markdown fences (```` ``` ```` or `~~~`) from the WANT group.

    **NOTE**: This is much better that just removing the fences from the source.
    Removing lines from the source will make useless the line numbers in the
    traceback.
    """
    _EXAMPLE_RE = re.compile(r'''
        # Source consists of a PS1 line followed by zero or more PS2 lines.
        (?P<source>
            (?:^(?P<indent> [ ]*) >>>    .*)    # PS1 line
            (?:\n           [ ]*  \.\.\. .*)*)  # PS2 lines
        \n?
        # Want consists of any non-blank lines that do not start with PS1.
        (?P<want> (?:(?![ ]*$)          # Not a blank line
                     (?![ ]*>>>)        # Not a line starting with PS1
                     (?![ ]*(```|~~~))  # Not a Markdown fence (ADDED LINE)
                     .+$\n?             # But any other line
                  )*)
        ''', re.MULTILINE | re.VERBOSE)
    

def testmod(m=None, name=None, globs=None, verbose=None,
            report=True, optionflags=0, extraglobs=None,
            raise_on_error=False, exclude_empty=False,
            parser=DocTestParser()):
    """ Same as [doctest.testmod](https://docs.python.org/3/library/doctest.html#doctest.testmod)
    but allows to specify a custom DocTestParser.

    All `master` related code is removed.
    """
    
    # If no module was given, then use __main__.
    if m is None:
        # DWA - m will still be None if this wasn't invoked from the command
        # line, in which case the following TypeError is about as good an error
        # as we should expect
        m = sys.modules.get('__main__')

    # Check that we were actually given a module.
    if not inspect.ismodule(m):
        raise TypeError("testmod: module required; %r" % (m,))

    # If no name was given, then use the module's name.
    if name is None:
        name = m.__name__

    # Find, parse, and run all tests in the given module.
    finder = DocTestFinder(exclude_empty=exclude_empty, parser=parser)

    if raise_on_error:
        runner = DebugRunner(verbose=verbose, optionflags=optionflags)
    else:
        runner = DocTestRunner(verbose=verbose, optionflags=optionflags)

    for test in finder.find(m, name, globs=globs, extraglobs=extraglobs):
        runner.run(test)

    if report:
        runner.summarize()

    return TestResults(runner.failures, runner.tries)
