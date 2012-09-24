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

buildrpm:
	python setup.py bdist_rpm

builddeb:
	debuild

clean:
	python setup.py clean
	$(MAKE) -f $(CURDIR)/debian/rules clean
	rm -rf build/ MANIFEST debian/source/ dist/
	find . -name '*.pyc' -delete

