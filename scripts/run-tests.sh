#! /bin/bash

set -e

pip install -q .
pytest -q test
