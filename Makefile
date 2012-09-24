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
	#To build a .deb package you have to rename pbsclusterviz-0.7b.tar.gz to
	#pbsclusterviz_0.7b.orig.tar.gz and place it the parent directory.
	#If you are having trouble, you might try to start from scratch:
	#apt-get install python python-dev python-dbg python-all python-all-dev python-all-dbg
	#py2dsc -m 'Paul Cochrane <paultcochrane@users.sourceforge.net>' ../pbsclusterviz-0.7b.tar.gz
	#python deb_dist/pbsclusterviz-0.7b/setup.py --command-packages=stdeb.command debianize
	#cp  ../pbsclusterviz-0.7b.tar.gz ../pbsclusterviz_0.7b.orig.tar.gz
	debuild

clean:
	python setup.py clean
	$(MAKE) -f $(CURDIR)/debian/rules clean
	rm -rf build/ MANIFEST debian/source/ dist/
	find . -name '*.pyc' -delete

