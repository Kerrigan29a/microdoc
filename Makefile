PY = $$(which python3 || which python)
URL = "https://github.com/kerrigan29a/microdoc/blob/main/{path}\#L{line}"

SOURCES = $(wildcard microdoc/*.py)

.PHONY: all clean test

all: test README.md

clean:
	rm -f README.md *.json
	rm -rf __pycache__ .mypy_cache

test:
	$(PY) -m unittest discover -v

README.md: README.md.in $(SOURCES)
			 (cat README.md.in | \
							 PYTHONPATH=. $(PY) -m microdoc.inject_usage) > README.md
			 ( PYTHONPATH=. $(PY) -m microdoc.py2doc $(SOURCES) | \
							 PYTHONPATH=. $(PY) -m microdoc.doc2md -l 2 -u $(URL) ) >> README.md
