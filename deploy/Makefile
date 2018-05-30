PACKAGE  = py-skel
DEST_DIR = debian/opt/teamin/py-skel
THREADS  = $(shell cat /proc/cpuinfo | grep ^processor | wc -l)

ifeq (0, $(shell git log -n1 --oneline | wc -l))
    # no git
    PATCH_VERSION = 0
    VERSION = 0
    GIT_HASH = 0000000
else
    BASE_VERSION = $(shell git rev-parse --abbrev-ref HEAD | sed -nr 's/^rel_(.+)\.[0-9a-f]{7,}$$/\1/p')
    ifeq (,$(BASE_VERSION))
        # not patch branch
        PATCH_VERSION = 0
        VERSION = $(shell git log --oneline | wc -l)
        GIT_HASH = $(shell git log -n1 --pretty=format:%h)
    else
        # patch branch
        BASE_HASH = $(shell git rev-parse --abbrev-ref HEAD | sed -nr 's/^rel_.+\.([0-9a-f]{7,})$$/\1/p')
        BASE_HASH_FULL = $(shell git log --pretty=format:%H | grep "^$(BASE_HASH)" | head -n1)

        PATCH_HASH = $(shell git log -n1 --pretty=format:%h)
        PATCH_VERSION = $(shell git log --oneline $(BASE_HASH_FULL).. | wc -l)
        VERSION = $(BASE_VERSION)
        GIT_HASH = $(BASE_HASH)
    endif
endif

ifeq (0, $(PATCH_VERSION))
    TARGET = $(PACKAGE)_$(VERSION).$(GIT_HASH).deb
else
    TARGET = $(PACKAGE)_$(VERSION).$(GIT_HASH).p$(PATCH_VERSION).deb
endif

.PHONY: $(PACKAGE) name version hash file root prepare clean distclean build

$(PACKAGE): root prepare
	fakeroot dpkg-deb -b debian $(TARGET)

name:
	@echo $(PACKAGE)

version:
	@if [ $(PATCH_VERSION) -eq 0 ]; then \
        echo $(VERSION); \
    else \
        echo $(VERSION).$(PATCH_VERSION); \
    fi

hash:
	@if [ $(PATCH_VERSION) -eq 0 ]; then \
        echo $(GIT_HASH); \
    else \
        echo $(GIT_HASH).$(PATCH_HASH); \
    fi

file:
	@echo $(TARGET)

root:
	@if [ $$(id -u) -eq 0 ]; then \
        echo; \
        echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"; \
        echo "+-------------------------------------------------------+"; \
        echo "+ Notice >>> Root privilege not required anymore!!! <<< +"; \
        echo "+-------------------------------------------------------+"; \
        echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"; \
        echo; \
        exit 1; \
    fi

prepare: clean
	mkdir -p $(DEST_DIR)/
	cp -r ../3rd ../bin ../src ../util ../test $(DEST_DIR)/
	cp ../config.yaml $(DEST_DIR)/config.sample.yaml
	cd $(DEST_DIR); find -type d -name __pycache__ | xargs -I{} rm -rf "{}"
	@sed -i -e "s/^Installed-Size:.*$$/Installed-Size: `du -s --exclude=DEBIAN debian | cut -f 1`/" debian/DEBIAN/control
	@if [ $(PATCH_VERSION) -eq 0 ]; then \
        sed -i -e "s/^Version:.*$$/Version: $(VERSION)/" \
            -e "s/^GitHash:.*$$/GitHash: $(GIT_HASH)/" \
            debian/DEBIAN/control; \
    else \
        sed -i -e "s/^Version:.*$$/Version: $(VERSION).$(PATCH_VERSION)/" \
            -e "s/^GitHash:.*$$/GitHash: $(GIT_HASH).$(PATCH_HASH)/" \
            debian/DEBIAN/control; \
    fi
	@find debian -type f |grep -v DEBIAN |xargs -I file md5sum file| sed s/debian\\//\\// > debian/DEBIAN/md5sums

clean:
	@sed -i -e "s/^Version:.*$$/Version:/" \
	    -e "s/^GitHash:.*$$/GitHash:/" \
        -e "s/^Installed-Size:.*$$/Installed-Size:/" \
        debian/DEBIAN/control
	rm -fr debian/opt
	rm -f  debian/DEBIAN/md5sums

distclean: clean
	rm -f *.deb
