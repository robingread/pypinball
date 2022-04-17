FROM ubuntu:20.04

COPY scripts /scripts
RUN apt-get update && \
  ./scripts/install-deps.sh && \
  ./scripts/setup-venv.sh
