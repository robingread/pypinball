FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
    alsa-base \
    alsa-utils \
    libsndfile1-dev \
    libx11-dev \
    libgl1-mesa-glx\
    xorg-dev  && \
    apt-get clean

COPY . pypinball
WORKDIR /pypinball
RUN apt-get update && \
    ./scripts/install-deps.sh && \
    pip install -r requirements.txt && \
    pip install .

