#! /bin/bash

set -e

source venv/bin/activate

echo "Running Python unittests & calculating code coverage..."

DATA_DIR=coverage
COVERAGE_REPORT=$DATA_DIR/.coverage
COVERAGE_REPORT_XML=$DATA_DIR/coverage.xml
TEST_REPORT=$DATA_DIR/test-report.xml

pip install -q .
coverage run --data-file=$COVERAGE_REPORT -m pytest -q test --junitxml=$TEST_REPORT
coverage report -m --data-file=$COVERAGE_REPORT
coverage xml -q --data-file=$COVERAGE_REPORT -o $COVERAGE_REPORT_XML