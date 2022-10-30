#! /usr/bin/bash

set -e

xhost +local:*

docker run \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
    --device /dev/snd \
    -it rread/pypinball:latest \
    python3 bin/controller.py