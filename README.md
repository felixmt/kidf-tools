# kidf-tools

## /!\ requires python 3.10

## py test
python3 -m pytest -k TestNavitiaHelper -q tests/tools/test_navitia_helper.py
python3 -m pytest -q tests/tools/*
python3 -m pytest -v --cov


## build package :
python3 setup.py sdist bdist_wheel
python3 setup.py sdist bdist_wheel && git add -A && git commit -m "commit" && git push -u origin main

## install libraries as pip package from other projects :
python3 -m pip install -e git+ssh://git@github.com/felixmt/kidf-tools.git#egg=tools --force-reinstall

## use package
from tools.sql_helper import sql_helper
