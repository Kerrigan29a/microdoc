# -*- coding: utf-8 -*-

# Copyright (c) Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

import sys
import subprocess

for line in sys.stdin:
    if "{{PY2DOC_USAGE}}" in line:
        output = subprocess.check_output([sys.executable, "py2doc.py", "-h"])
        line = line.replace("{{PY2DOC_USAGE}}", output.rstrip().decode("utf-8"))
        line = f"```\n{line}```\n"
    elif "{{DOC2MD_USAGE}}" in line:
        output = subprocess.check_output([sys.executable, "doc2md.py", "-h"])
        line = line.replace("{{DOC2MD_USAGE}}", output.rstrip().decode("utf-8"))
        line = f"```\n{line}```\n"
    elif "{{MD2HTML_USAGE}}" in line:
        output = subprocess.check_output([sys.executable, "md2html.py", "-h"])
        line = line.replace("{{MD2HTML_USAGE}}", output.rstrip().decode("utf-8"))
        line = f"```\n{line}```\n"
    sys.stdout.write(line)
