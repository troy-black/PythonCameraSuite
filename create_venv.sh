#!/bin/bash

# enable verbose and exit on error
set -ex

# (re)create local venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# update pip
pip install --upgrade pip
pip install --upgrade setuptools
pip install --upgrade wheel

# install project in dev mode
pip install -v -e .[all]
