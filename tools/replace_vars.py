#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

import sys
import subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from microdoc import __version__


for line in sys.stdin:
    if "{{PY2DOC_USAGE}}" in line:
        output = subprocess.check_output(
            [sys.executable, "-m", "microdoc.py2doc", "-h"]
        )
        line = line.replace("{{PY2DOC_USAGE}}", output.rstrip().decode("utf-8"))
        line = f"```\n{line}```\n"
    elif "{{DOC2MD_USAGE}}" in line:
        output = subprocess.check_output(
            [sys.executable, "-m", "microdoc.doc2md", "-h"]
        )
        line = line.replace("{{DOC2MD_USAGE}}", output.rstrip().decode("utf-8"))
        line = f"```\n{line}```\n"
    elif "{{MD2HTML_USAGE}}" in line:
        output = subprocess.check_output(
            [sys.executable, "-m", "microdoc.md2html", "-h"]
        )
        line = line.replace("{{MD2HTML_USAGE}}", output.rstrip().decode("utf-8"))
        line = f"```\n{line}```\n"
    elif "{{VERSION}}" in line:
        line = line.replace("{{VERSION}}", __version__)
    sys.stdout.write(line)
