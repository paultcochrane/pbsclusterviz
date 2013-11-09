.PHONY: help doc api pylint dist

help:
	@echo "Possible make targets: doc, pylint, dist, deb, rpm"

doc:
	cd doc; $(MAKE) html

pylint:
	pylint --rcfile=pylint.rc pbsclusterviz

dist:
	python setup.py sdist

VERSION=0.7a
RPMBUILD_DIR=$(HOME)/rpmbuild
rpm: dist
	mkdir -p $(RPMBUILD_DIR)
	mkdir -p $(RPMBUILD_DIR)/BUILD
	mkdir -p $(RPMBUILD_DIR)/BUILDROOT
	mkdir -p $(RPMBUILD_DIR)/RPMS
	mkdir -p $(RPMBUILD_DIR)/SOURCES
	mkdir -p $(RPMBUILD_DIR)/SPECS
	mkdir -p $(RPMBUILD_DIR)/SRPMS
	cp rpm/pbsclusterviz.spec $(RPMBUILD_DIR)/SPECS/
	cp dist/pbsclusterviz-$(VERSION).tar.gz $(RPMBUILD_DIR)/SOURCES/
	rpmbuild -ba $(RPMBUILD_DIR)/SPECS/pbsclusterviz.spec

DEBUILD_DIR=/tmp/pbsclusterviz_debuild
deb: dist
	mkdir -p $(DEBUILD_DIR)
	cp dist/pbsclusterviz-$(VERSION).tar.gz $(DEBUILD_DIR)/pbsclusterviz_$(VERSION).orig.tar.gz
	tar -C $(DEBUILD_DIR) -xvzf $(DEBUILD_DIR)/pbsclusterviz_$(VERSION).orig.tar.gz
	cp -r debian $(DEBUILD_DIR)/pbsclusterviz-$(VERSION)/
	cd $(DEBUILD_DIR)/pbsclusterviz-$(VERSION)/debian; debuild -us -uc
	cp $(DEBUILD_DIR)/python-pbsclusterviz_$(VERSION)-1_all.deb dist
	cd $(DEBUILD_DIR); sudo pbuilder --build pbsclusterviz_0.7a-1.dsc
	@echo "Now check the .deb file in /var/cache/pbuilder/result"

clean:
	python setup.py clean
	find . -name '*.pyc' -delete
	rm -rf $(DEBUILD_DIR)
