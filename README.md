# Pi-Pinball


[![pipeline status](https://gitlab.com/robin.g.read/pypinball/badges/dev/pipeline.svg)](https://gitlab.com/robin.g.read/pypinball/-/commits/dev)
[![coverage report](https://gitlab.com/robin.g.read/pypinball/badges/dev/coverage.svg)](https://gitlab.com/robin.g.read/pypinball/-/commits/dev)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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
- Build all documentation locally in the `docs` directory.

## Documentation

Pre-built documentation can be found at [https://robin.g.read.gitlab.io/pypinball/index.html](https://robin.g.read.gitlab.io/pypinball/index.html). 
To build the documentation locally, run:

```bash
source venv/bin/activate
./scripts/build-docs.sh
```

## Gitlab CI Variables

| Name | Default | Description |
|---|---|---|
| `BUILD_DOCKER_IMAGE` | "false" | Whether to build a Docker image. This can be used to build a Docker image only once a day and use that image throughout the day rather than needing to build it on each CI run. |
