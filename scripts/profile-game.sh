#! /bin/bash

set -e

OUTPUT_FILE=profile_output
python -m cProfile -o $OUTPUT_FILE bin/pypinball
snakeviz $OUTPUT_FILE