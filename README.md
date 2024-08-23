# Pi-Pinball

[![ci tests](https://github.com/robingread/pypinball/actions/workflows/ci-test-pipeline.yaml/badge.svg)](https://github.com/robingread/pypinball/actions/workflows/ci-test-pipeline.yaml)
[![coverage report](https://gitlab.com/robin.g.read/pypinball/badges/master/coverage.svg)](https://gitlab.com/robin.g.read/pypinball/-/commits/master)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

## Overview
The game is installed as a python package, `pypinball`, which can be called from the command line.

### Controls

The game assumes that there are three buttons, *left*, *right* and *centre*.

When playing on a keyboard, the mapping is:
- left -> **f**
- right -> **j**
- centre -> **sparebar**

## Setup

Install dependencies:

```bash
./scripts/install-deps.sh
```

To start development first setup the `virtualenv`:

```bash
./scripts/setup-venv.sh
```

## Testing

To run the testing suite:

```bash
./scripts/ci-test.sh
```

This test suite will:

- Remove all installed instances of `pypinball`.
- Check that the code adheres to the [`black`](https://black.readthedocs.io/en/stable/) formatting standard.
- Run all unit-tests in the `test` directory.