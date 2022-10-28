#! /bin/bash

set -e
source venv/bin/activate
pylint --rcfile .pylintrc pypinball || true