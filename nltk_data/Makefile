PYTHON = python3
BASEURL = https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages

pkg_index:
	$(PYTHON) tools/build_collections.py .
	$(PYTHON) tools/build_pkg_index.py . $(BASEURL) index.xml
	git add index.xml collections

grammars:
	git commit -m "updated grammar files" packages/grammars

