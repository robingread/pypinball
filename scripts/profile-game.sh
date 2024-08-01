#! /bin/bash

set -e

# Adding to the coverage directory as that is included in the .gitignore file
OUTPUT_FILE="coverage/profile_output.prof"

if [ -f $OUTPUT_FILE ]; then
    echo "Deleting old output file:" $OUTPUT_FILE
    rm $OUTPUT_FILE
fi

python scripts/run_profiler.py ${OUTPUT_FILE}
snakeviz ${OUTPUT_FILE}