#! /bin/bash

set -e

pip install .
pytest test
