# Pi-Pinball

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
| `BUILD_DOCKER_IMAGE` | "true" | Whether to build a Docker image. This can be used to build a Docker image only once a day and use that image throughout the day rather than needing to build it on each CI run. |
