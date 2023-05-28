#! /bin/bash

set -eu

BUILDER_NAME=multi-arch
IMG=robingread/pypinball
TAG=${1}

echo "Deploying docker image with tag:" ${IMG}:${TAG}

export DOCKER_CLI_EXPERIMENTAL=enabled

docker buildx create --name $BUILDER_NAME --use || true
docker buildx inspect --bootstrap

# Skipping linux/arm/v7
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t $IMG:$TAG \
    -t $IMG:latest \
    -f Dockerfile \
    --push ..