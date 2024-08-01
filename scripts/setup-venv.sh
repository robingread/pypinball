#! /bin/bash

set -eu

if ! which virtualenv &> /dev/null
then
  echo "Installing virtual env..."
  pip install virtualenv
else
  echo "Virtualenv found and already installed"
fi

DST_DIR=./venv
WHICH_PYTHON=`which python3`

echo "Setting up Virtual Python environment"
echo "Python path:" $WHICH_PYTHON
echo "Destination dir:" $DST_DIR

virtualenv --clear --python $WHICH_PYTHON $DST_DIR --prompt pypinball

source $DST_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
