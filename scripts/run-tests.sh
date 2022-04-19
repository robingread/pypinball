#! /bin/bash

set -e

pip install .
pytest -q test
