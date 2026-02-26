# Use a lightweight Python base image
# Python >=3.13 is required by codespeak-cli
FROM python:3.13-slim

# Copy uv binaries from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies
# Git is required for 'codespeak init'
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash codespeak

# Set the working directory
WORKDIR /app
RUN chown codespeak:codespeak /app

# Copy the proxy script for auth flow to a location not shadowed by volumes
COPY --chmod=755 auth_proxy.py /usr/local/bin/auth_proxy

# Switch to the non-root user
USER codespeak
ENV HOME=/home/codespeak
ENV PATH="${HOME}/.local/bin:${PATH}"

# Install codespeak-cli using uv
RUN uv tool install codespeak-cli

# Expose the proxy port
EXPOSE 8081

# Set codespeak as the entrypoint so the container acts as the CLI
ENTRYPOINT ["codespeak"]

