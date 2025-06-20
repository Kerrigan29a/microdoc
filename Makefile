PYTHON := $(shell which python3 || which python)
URL := "https://github.com/kerrigan29a/microdoc/blob/main/{path}\#L{line}"
SOURCES := $(wildcard microdoc/*.py)

.PHONY: all clean test release

all: test README.md

clean:
	-rm -f README.md *.json
	-rm -rf .mypy_cache
	-find . -name '*.pyc' -delete
	-find . -name '__pycache__' -delete

test:
	$(PYTHON) -m unittest discover -v

README.md: README.md.in $(SOURCES)
	cat README.md.in | $(PYTHON) tools/replace_vars.py > README.md
	$(PYTHON) -m microdoc.py2doc $(SOURCES) | $(PYTHON) -m microdoc.doc2md -l 2 -u $(URL) >> README.md

release: all
	VERSION=$$($(PYTHON) -c 'import microdoc; print(microdoc.__version__)') && \
	git push origin main && \
	git tag -a v$$VERSION -m "Release v$$VERSION" && \
	git push origin --tags
