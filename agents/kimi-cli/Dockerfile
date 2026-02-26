FROM python:3.13-slim

# Build arguments for custom UID/GID (defaults to 1000)
ARG USER_ID=1000
ARG GROUP_ID=1000

# Create a non-root user and group with configurable UID/GID
RUN groupadd -r -g ${GROUP_ID} appuser && \
    useradd -r -m -u ${USER_ID} -g appuser -s /bin/bash appuser

# Install system utilities
RUN apt-get update && \
    apt-get install -y git ripgrep curl iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Create app directory and set ownership to the non-root user
RUN mkdir -p /app && chown -R appuser:appuser /app
WORKDIR /app

# Ensure appuser's local bin is on PATH and writable
RUN mkdir -p /home/appuser/.local/bin && \
    chown -R appuser:appuser /home/appuser/.local
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Switch to non-root user
USER appuser

# Install kimi-cli using uv (official recommended method)
RUN uv tool install --python 3.13 kimi-cli

# Set the entrypoint to run kimi
ENTRYPOINT [ "kimi" ]
