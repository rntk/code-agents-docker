# OCI labels for metadata
ARG VCS_REF=""
ARG BUILD_DATE=""
ARG VERSION=""

FROM ubuntu:24.04

# Install system utilities and Java (required for JetBrains tools)
RUN apt-get update && apt-get install -y \
    git \
    ripgrep \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Install Junie CLI as root (installs to system location)
ARG JUNIE_VERSION=latest
RUN curl -fsSL https://junie.jetbrains.com/install.sh | bash

WORKDIR /app

# Change ownership of app directory to ubuntu user (UID 1000 already exists)
RUN chown -R ubuntu:ubuntu /app
RUN mkdir -p /home/ubuntu/.junie && \
  chown -R ubuntu:ubuntu /home/ubuntu/.junie

# Switch to ubuntu user
USER ubuntu

ENTRYPOINT ["junie"]
