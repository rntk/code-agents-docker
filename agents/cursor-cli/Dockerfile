# OCI labels for metadata
ARG VCS_REF=""
ARG BUILD_DATE=""
ARG VERSION=""

FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    git \
    ripgrep \
    curl \
    iputils-ping \
    unzip \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/home/ubuntu/.local/bin:${PATH}"

USER ubuntu

RUN curl -fsSL https://cursor.com/install | bash

WORKDIR /app

USER root
RUN chown -R ubuntu:ubuntu /app
USER ubuntu

ENTRYPOINT ["agent"]
