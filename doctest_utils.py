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
__version__ = "0.5.0"
__license__ = "BSD 3-Clause Clear License"

from doctest import DocTestFinder, DocTestParser, DebugRunner, DocTestRunner, TestResults
import inspect
import re
import sys


class MarkdownDocTestParser(DocTestParser):
    """A [doctest.DocTestParser](https://docs.python.org/3/library/doctest.html#doctest.DocTestParser)
    that removes code blocks from Markdown files before parsing them.
    
    This allows to write Markdown files with code blocks that can be tested with
    [doctest](https://docs.python.org/3/library/doctest.html).
    """
    def parse(self, string, name='<string>'):
        string = re.sub(r'^\s*(```|~~~)\s*.*$', '', string, flags=re.MULTILINE)
        return super().parse(string, name)
    

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
