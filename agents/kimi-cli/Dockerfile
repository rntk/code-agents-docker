FROM python:3.13-slim

# Build arguments for custom UID/GID (defaults to 1000)
ARG USER_ID=1000
ARG GROUP_ID=1000

# Install system utilities
RUN apt-get update && \
    apt-get install -y git ripgrep curl iputils-ping && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user and group with configurable UID/GID
RUN groupadd -r -g ${GROUP_ID} appuser && \
    useradd -r -m -u ${USER_ID} -g appuser -s /bin/bash appuser

# Create app directory and set ownership to the non-root user
RUN mkdir -p /app && chown -R appuser:appuser /app
WORKDIR /app

# Ensure appuser's local and cargo bins are on PATH
ENV PATH="/home/appuser/.cargo/bin:/home/appuser/.local/bin:${PATH}"

# Switch to non-root user
USER appuser

# Install kimi-cli using the official installation script
RUN curl -LsSf https://code.kimi.com/install.sh | bash

# Set the entrypoint to run kimi
ENTRYPOINT [ "kimi" ]
