#! /usr/bin/bash

set -eu

IMG=robingread/pypinball:latest

xhost +local:*

docker run \
    --name pypinball \
    -e DISPLAY=$DISPLAY \
    -e LIBGL_ALWAYS_SOFTWARE=1 \
    -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
    --device /dev/snd \
    -it ${IMG} \
    pypinball