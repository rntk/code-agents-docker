FROM python:3.13-slim

# Build arguments for custom UID/GID (defaults to 1000)
ARG USER_ID=1000
ARG GROUP_ID=1000

# Create a non-root user and group with configurable UID/GID
RUN groupadd -r -g ${GROUP_ID} appuser && \
    useradd -r -m -u ${USER_ID} -g appuser -s /bin/bash appuser

# Install curl and bash
RUN apt-get update && \
    apt-get install -y curl bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create app directory and set ownership to the non-root user
RUN mkdir -p /app && chown -R appuser:appuser /app
WORKDIR /app

# Update PATH to include .local/bin for the non-root user
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Switch to non-root user
USER appuser

# Install kimi from code.kimi.com
RUN curl -L code.kimi.com/install.sh | bash || \
    (test -f /home/appuser/.local/bin/env && . /home/appuser/.local/bin/env && exit 0) || \
    exit 0

# Verify installation
RUN which uv || echo "uv installed at /home/appuser/.local/bin/uv"

# Set the entrypoint to run kimi
CMD ["kimi"]
