#! /bin/bash

set -e

DST_DIR=./venv

virtualenv --clear --python /usr/bin/python3 $DST_DIR

source $DST_DIR/bin/activate
pip install --upgrade pip
