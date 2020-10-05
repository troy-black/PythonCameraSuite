#!/bin/bash

set -ex

source venv/bin/activate

coverage run --source=tdb/ -m unittest discover tests/

coverage html

open htmlcov/index.html
