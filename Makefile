PY = $$(which python3 || which python)
URL = "https://github.com/kerrigan29a/microdoc/blob/main/{path}\#L{line}"

.PHONY: all clean

all: README.md

README.md: README.md.in py2doc.py doc2md.py
	cat README.md.in > README.md
	( $(PY) py2doc.py py2doc.py doc2md.py | \
	$(PY) doc2md.py -l 2 -u $(URL) | \
	$(PY) inject_usage.py ) >> README.md
	
clean:
	rm -f README.md doc.json
