# Makefile for Python project.

prefix ?= /usr
INSTALL ?= install
RM ?= rm -f

PYTHON ?= python3
SHEBANG ?= "/usr/bin/env $(PYTHON)"

PYLINT ?= pylint
MYPY ?= mypy

SRCDIR = src
OUTFILE = xsnap

ifeq ($(VERBOSE),1)
V :=
else
V := @
endif

all: binary

.PHONY: binary
binary:
	$(V)$(PYTHON) -m zipapp -c -o $(OUTFILE) -p $(SHEBANG) $(SRCDIR)

# .PHONY: check
# check: lint mypy codestyle

.PHONY: lint
lint:
	-$(V)$(PYLINT) $(SRCDIR)

.PHONY: mypy
mypy:
	-$(V)$(MYPY) --strict $(SRCDIR)

.PHONY: codestyle
codestyle:
	-$(V)$(PYTHON) -m pycodestyle $(SRCDIR)

.PHONY: clean
clean:
	-$(V)$(RM) $(OUTFILE)

.PHONY: distclean
distclean: clean
	-$(V)$(RM) $(OUTFILE)

.PHONY: install
install: binary
	$(V)$(INSTALL) -D $(OUTFILE) $(DESTDIR)$(prefix)/bin/$(OUTFILE)

# --------------------------------------------------------------------------- #
# Packaging                                                                   #
# --------------------------------------------------------------------------- #

.PHONY: clean
arch: clean
	$(V)set -e; \
		project=`basename \`pwd\``; \
		timestamp=`date '+%Y-%m-%d-%H%M%S'`; \
		destfile=../$$project-$$timestamp.tar.zst; \
		tar -C .. -caf $$destfile $$project && chmod 444 $$destfile; \
		echo -n "$$destfile" | xclip -selection clipboard -i; \
		echo "Archive is $$destfile"

.PHONY: build-deb
build-deb: clean
	$(V)which dpkg-buildpackage || \
		{ echo "\e[91mPackage dpkg-dev not installed\e[0m"; exit 1; }
	$(V)./debian/rules clean
	$(V)dpkg-buildpackage --build=binary --unsigned-changes --unsigned-source

.PHONY: build-dist
build-dist:
	$(V)$(PYTHON3) bdist bdist_wheel

# vim: set ts=8 noet sts=8:
