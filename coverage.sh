#/usr/bin/env bash

export PYTHONPATH='.'

coverage erase
coverage run fix_coverage.py
testify tests -c $@
coverage combine
coverage report -m --omit=/usr/*,*/__init__.py,tests/*,pre-commit.py
exit $?
