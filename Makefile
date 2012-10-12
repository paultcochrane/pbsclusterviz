.PHONY: help doc api pylint dist

help:
	@echo "Possible make targets: doc, pylint, wwwsync, dist, builddeb, buildrpm"

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

DEBUILD_DIR=/tmp/pbsclusterviz_debuild
VERSION=0.7a
builddeb: dist
	mkdir $(DEBUILD_DIR)
	cp dist/pbsclusterviz-$(VERSION).tar.gz $(DEBUILD_DIR)/pbsclusterviz_$(VERSION).orig.tar.gz
	tar -C $(DEBUILD_DIR) -xvzf $(DEBUILD_DIR)/pbsclusterviz_$(VERSION).orig.tar.gz
	cp -r debian $(DEBUILD_DIR)/pbsclusterviz-$(VERSION)/
	cd $(DEBUILD_DIR)/pbsclusterviz-$(VERSION)/debian; debuild -us -uc
	cp $(DEBUILD_DIR)/python-pbsclusterviz_$(VERSION)-1_all.deb dist

clean:
	python setup.py clean
	find . -name '*.pyc' -delete
	rm -rf $(DEBUILD_DIR)
