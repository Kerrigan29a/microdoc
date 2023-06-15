PY = $$(which python3 || which python)

.PHONY: all clean

all: README.md

README.md: README.md.in py2doc.md doc2md.md
	cat README.md.in py2doc.md doc2md.md > README.md

py2doc.md: py2doc.py
	$(PY) py2doc.py -i py2doc.py | $(PY) doc2md.py -o py2doc.md

doc2md.md:  doc2md.py
	$(PY) py2doc.py -i doc2md.py | $(PY) doc2md.py -o doc2md.md

clean:
	rm -f README.md py2doc.md doc2md.md
	rm -f py2doc.doc doc2md.doc