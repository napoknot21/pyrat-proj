#!/bin/sh

# Create a virtual environment in a subdirectory named venv
python3 -m venv .

# Activate the virtual environment
# source ./bin/activate

# Modify the pyvenv.cfg file
sed -i "s/false/true/g" ./pyvenv.cfg

# Install the PyRat package
pip install ./extras/PyRat

# Run the setup_workspace function from the pyrat module
python -c "import pyrat; pyrat.PyRat.setup_workspace()" 2> /dev/null
