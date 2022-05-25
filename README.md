# Pi-Pinball


[![pipeline status](https://gitlab.com/robin.g.read/pypinball/badges/dev/pipeline.svg)](https://gitlab.com/robin.g.read/pypinball/-/commits/dev)
[![coverage report](https://gitlab.com/robin.g.read/pypinball/badges/dev/coverage.svg)](https://gitlab.com/robin.g.read/pypinball/-/commits/dev)

## Setup

Install dependencies:

```bash
./scripts/install-deps.sh
```

To develop, setup the virtualenv:

```bash
./scripts/setup-venv.sh
```

## Testing

To run the testing suite:

```bash
./scripts/ci-test.sh
```

## Documentation

To build the documentation, run:

```bash
source venv/bin/activate
./scripts/build-docs.sh
```

## Gitlab CI Variables

| Name | Default | Description |
|---|---|---|
| `BUILD_DOCKER_IMAGE` | "false" | Whether to build a Docker image. This can be used to build a Docker image only once a day and use that image throughout the day rather than needing to build it on each CI run. |
