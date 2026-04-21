# OCI labels for metadata
ARG VCS_REF=""
ARG BUILD_DATE=""
ARG VERSION=""

FROM ubuntu:24.04

# Install system utilities
RUN apt-get update && apt-get install -y \
    git \
    ripgrep \
    curl \
    iputils-ping \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN chown -R ubuntu:ubuntu /app

# Installer places launcher in ~/.local/bin
ENV PATH=/home/ubuntu/.local/bin:$PATH

# Switch to non-root user before installing
USER ubuntu

RUN curl -fsSL https://claude.ai/install.sh | bash

ENTRYPOINT ["claude"]
