# syntax=docker/dockerfile:1.7
FROM node:24-alpine

# OCI labels and build metadata
ARG VCS_REF=""
ARG BUILD_DATE=""
ARG VERSION=""

ENV NODE_ENV=production \
    NPM_CONFIG_FUND=false \
    NPM_CONFIG_AUDIT=false \
    NPM_CONFIG_UPDATE_NOTIFIER=false

# Minimal runtime packages and basic shell utilities
RUN apk add --no-cache \
    ca-certificates \
    coreutils \
    bash \
    findutils \
    grep \
    sed \
    gawk

# Configure Codex CLI version via build-arg
ARG CODEX_VERSION=latest

# Install Codex CLI globally with BuildKit cache and clean npm cache
RUN --mount=type=cache,target=/root/.npm \
    npm install -g "@openai/codex@${CODEX_VERSION}" \
 && npm cache clean --force

# Drop privileges
USER node
WORKDIR /app

# Use ENTRYPOINT so additional args are passed to codex by default
ENTRYPOINT ["codex"]
