#! /usr/bin/bash

set -eu

TAG=${1:-latest}
IMG=robingread/pypinball:${TAG}

xhost +local:*

docker run \
    --name pypinball \
    --rm \
    -e DISPLAY=$DISPLAY \
    -e LIBGL_ALWAYS_SOFTWARE=1 \
    -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
    --device /dev/snd \
    -it ${IMG} \
    pypinball