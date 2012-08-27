.PHONY: help doc api pylint dist

help:
	@echo "Possible make targets: doc, api, pylint, wwwsync, dist"

doc:
	cd doc; $(MAKE) html

api:
	epydoc --html -o api/ --graph=all -n "PBS Cluster Viz" pbsclusterviz

pylint:
	pylint --rcfile=pylint.rc pbsclusterviz

wwwsync:
	rsync -avz doc/_build/html/ paultcochrane@web.sourceforge.net:/home/project-web/pbsclusterviz/htdocs/

dist:
	python setup.py sdist
