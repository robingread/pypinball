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

DIRECTORIES=(
  pypinball/
  test/
  scripts/
)

if [ "$RUN_CHECK" = true ]
then
  echo "Running isort check..."
  isort --profile black --check "${DIRECTORIES[@]}"
  echo "Running black formatter check..."
  black --check --diff --color "${DIRECTORIES[@]}"
else
  echo "Running isort..."
  isort --profile black "${DIRECTORIES[@]}"
  echo "Running black formatter..."
  black "${DIRECTORIES[@]}"
fi
