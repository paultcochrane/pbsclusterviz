.PHONY: help doc api pylint dist

help:
	@echo "Possible make targets: doc, pylint, wwwsync, dist"

doc:
	cd doc; $(MAKE) html

pylint:
	pylint --rcfile=pylint.rc pbsclusterviz

wwwsync:
	rsync -avz doc/_build/html/ paultcochrane@web.sourceforge.net:/home/project-web/pbsclusterviz/htdocs/

dist:
	python setup.py sdist
