#!/bin/sh

relpath=`dirname $0`
abspath=`realpath "${relpath}"`

# cd "${abspath}" && python3 -c 'print("a")' -m "src" $*
PYTHONPATH="${abspath}" python3 -B -m "src" $*

# vim: set sts=4 et sw=4:
