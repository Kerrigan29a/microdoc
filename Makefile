PY = $$(which python3 || which python)

.PHONY: all clean

all: README.md

README.md: README.md.in py2doc.py doc2md.py
	cat README.md.in > README.md
	($(PY) py2doc.py py2doc.py doc2md.py | $(PY) doc2md.py) >> README.md
	
clean:
	rm -f README.md doc.json
