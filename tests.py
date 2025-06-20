# -*- coding: utf-8 -*-

# Copyright (c) Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

import unittest
import doctest
from microdoc import doctest_utils
from microdoc import py2doc
from microdoc import doc2md

"""
It loads the [doctest](https://docs.python.org/3/library/doctest) and [expose
them as unittests](https://docs.python.org/3/library/doctest.html#unittest-api).
"""


def load_tests(loader, tests, ignore):
    parser = doctest_utils.MarkdownDocTestParser()
    test_finder = doctest.DocTestFinder(parser=parser)
    tests.addTests(doctest.DocTestSuite(py2doc, test_finder=test_finder))
    tests.addTests(doctest.DocTestSuite(doc2md, test_finder=test_finder))
    # tests.addTests(doctest.DocFileSuite("../README.md.in",
    #                                     globs={**py2doc.__dict__, **doc2md.__dict__}},
    #                                     parser=MarkdownTestParser()))
    return tests
