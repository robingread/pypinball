#! /bin/bash

set -e

apt-get update

apt-get install -y \
  libasound2-dev \
  python3-dev \
  python3-pip

pip install virtualenv
