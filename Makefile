
docs: README.md docs_src
	sphinx-apidoc -f -o ./docs_src yahoo_auction_auto
	sphinx-build docs_src docs

test: flake8 mypy unittest

flake8:
	flake8 .

mypy:
	mypy .

unittest:
	coverage run -m unittest
	coverage html
	coverage report
