#! /bin/bash

set -eu

source venv/bin/activate

RUN_CHECK=false

while getopts c flag
do
  case "${flag}" in
    c) RUN_CHECK=true;;
    *) echo "Unknown options...";;
  esac
done

SRC_DIR=pypinball/
TEST_DIR=test/

if [ "$RUN_CHECK" = true ]
then
  echo "Running isort check..."
  isort --profile black --check $SRC_DIR $TEST_DIR
  echo "Running black formatter check..."
  black --check --diff --color $SRC_DIR $TEST_DIR
else
  echo "Running isort..."
  isort --profile black $SRC_DIR $TEST_DIR
  echo "Running black formatter..."
  black $SRC_DIR $TEST_DIR
fi
