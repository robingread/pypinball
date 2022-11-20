#! /bin/bash

set -e

if ! which virtualenv &> /dev/null
then
  echo "Installing virtual env..."
  pip install virtualenv
else
  echo "Virtualenv found and already installed"
fi

DST_DIR=./venv
virtualenv --clear --python `which python3` $DST_DIR

source $DST_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
