# -*- coding: utf-8 -*-

# Copyright (c) 2023 Javier Escalada Gómez
# All rights reserved.
# License: BSD 3-Clause Clear License (see LICENSE for details)

import sys
import subprocess

for line in sys.stdin:
    if "{{DOC2MD_USAGE}}" in line:
        output = subprocess.check_output([sys.executable, "doc2md.py", "-h"])
        line = line.replace("{{DOC2MD_USAGE}}", output.decode("utf-8"))
        line = f"```\n{line}```"
    elif "{{PY2DOC_USAGE}}" in line:
        output = subprocess.check_output([sys.executable, "py2doc.py", "-h"])
        line = line.replace("{{PY2DOC_USAGE}}", output.decode("utf-8"))
        line = f"```\n{line}```"
    sys.stdout.write(line)
