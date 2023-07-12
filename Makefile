PY = $$(which python3 || which python)
URL = "https://github.com/kerrigan29a/microdoc/blob/main/{path}\#L{line}"

SOURCES = $(wildcard *.py)

.PHONY: all clean test

all: test README.md

test:
	$(PY) -m unittest discover -v

README.md: README.md.in $(SOURCES)
	(cat README.md.in | \
		$(PY) inject_usage.py) > README.md
	( $(PY) py2doc.py $(SOURCES) | \
		$(PY) doc2md.py -l 2 -u $(URL) ) >> README.md
	
clean:
	rm -f README.md *.json
