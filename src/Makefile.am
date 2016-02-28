## Process this file with automake to produce Makefile.in
## Created by Anjuta


uidir = $(pkgdatadir)/ui
ui_DATA = wavplusmp3.ui


## The main script
bin_SCRIPTS = wavplusmp3.py

## Directory where .class files will be installed
wavplusmp3dir = $(pythondir)/wavplusmp3


wavplusmp3_PYTHON = \
	wavplusmp3.py


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(pkgdatadir)
