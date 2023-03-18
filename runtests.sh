#! /bin/bash

flake8 modules --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 modules --count --max-complexity=10 --max-line-length=127 --statistics

nosetests -v --with-spec --spec-color --with-coverage --cover-package=modules
