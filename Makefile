PYTHON = $$(which python3 || which python)
URL = "https://github.com/kerrigan29a/microdoc/blob/main/{path}\#L{line}"

SOURCES = $(wildcard microdoc/*.py)

.PHONY: all clean test

all: test README.md

clean:
	rm -f README.md *.json
	rm -rf __pycache__ .mypy_cache

test:
	$(PYTHON) -m unittest discover -v

README.md: README.md.in $(SOURCES)
	cat README.md.in | $(PYTHON) -m microdoc.inject_usage > README.md
	$(PYTHON) -m microdoc.py2doc $(SOURCES) | $(PYTHON) -m microdoc.doc2md -l 2 -u $(URL) >> README.md
