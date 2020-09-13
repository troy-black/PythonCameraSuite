#!/bin/bash

# enable echo
set -x

# (re)create local venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# update pip
pip install --upgrade pip setuptools wheel

# install project in dev mode
pip install -e .[all]
