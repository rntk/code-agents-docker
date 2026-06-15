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

# Switch to ubuntu user so the install script runs as non-root
USER ubuntu

# Install Grok CLI (downloads binary into ~/.grok/downloads and links ~/.grok/bin)
RUN curl -fsSL https://x.ai/cli/install.sh | bash

# Copy the actual binary to a system directory so it survives the host ~/.grok bind-mount at runtime
USER root
RUN platform_file=$(ls /home/ubuntu/.grok/downloads/grok-linux-*) && \
    cp "$platform_file" /usr/local/bin/grok && \
    cp "$platform_file" /usr/local/bin/agent && \
    chmod +x /usr/local/bin/grok /usr/local/bin/agent && \
    chown -R ubuntu:ubuntu /app
USER ubuntu

ENTRYPOINT ["grok"]
