# -*- coding: utf-8 -*-

# Copyright (c) Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

import sys
from contextlib import contextmanager


@contextmanager
def reader(input):
    """Open the input file, or stdin if not specified."""
    if input is None:
        yield sys.stdin
    else:
        with open(input, mode="r", encoding="utf-8") as f:
            yield f


@contextmanager
def writer(output):
    """Open the output file, or stdout if not specified."""
    if output is None:
        yield sys.stdout
    else:
        with open(output, mode="w", encoding="utf-8") as f:
            yield f
