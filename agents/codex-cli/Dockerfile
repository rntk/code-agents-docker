# syntax=docker/dockerfile:1.7
FROM node:24-slim

# OCI labels and build metadata
ARG VCS_REF=""
ARG BUILD_DATE=""
ARG VERSION=""

ENV NODE_ENV=production \
    NPM_CONFIG_FUND=false \
    NPM_CONFIG_AUDIT=false \
    NPM_CONFIG_UPDATE_NOTIFIER=false

# Install system utilities
RUN apt-get update && apt-get install -y \
    git \
    ripgrep \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/node/.npm-global && \
    chown -R node:node /home/node/.npm-global

# Set npm global prefix to user-writable directory
ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
ENV PATH="/home/node/.npm-global/bin:${PATH}"

# Drop privileges before installing
USER node
WORKDIR /app

# Configure Codex CLI version via build-arg
ARG CODEX_VERSION=latest

# Install Codex CLI globally with BuildKit cache
RUN --mount=type=cache,uid=1000,gid=1000,target=/home/node/.npm \
    npm install -g "@openai/codex@${CODEX_VERSION}" \
 && npm cache clean --force

# Use ENTRYPOINT so additional args are passed to codex by default
ENTRYPOINT ["codex"]
