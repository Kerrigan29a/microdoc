PY = $$(which python3 || which python)
URL = "https://github.com/kerrigan29a/microdoc/blob/main/{path}\#L{line}"

SOURCES = $(wildcard microdoc/*.py)

.PHONY: all clean test

all: test README.md

test:
	$(PY) -m unittest discover -v

README.md: README.md.in $(SOURCES)
       (cat README.md.in | \
               $(PY) -m microdoc.inject_usage) > README.md
       ( $(PY) -m microdoc.py2doc $(SOURCES) | \
               $(PY) -m microdoc.doc2md -l 2 -u $(URL) ) >> README.md

clean:
	rm -f README.md *.json
