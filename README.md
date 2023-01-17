# kidf-tools
build package :
python3 setup.py sdist bdist_wheel

install libraries as pip package from other projects :
python3 -m pip install -e git+ssh://git@github.com/felixmt/kidf-tools.git#egg=verysimplemodule --force-reinstall