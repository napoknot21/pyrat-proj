#!/bin/sh

python3 -m venv .

source ./bin/activate

sed -i "s/false/true/g" pyvenv.cfg

export PATH=$PATH:$PWD/bin/

python3 -m pip install --user ./extras/PyRat

./bin/python3 -c "import pyrat; pyrat.PyRat.setup_workspace()" 2> /dev/null
