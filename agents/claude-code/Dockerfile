# OCI labels for metadata
ARG VCS_REF=""
ARG BUILD_DATE=""
ARG VERSION=""

FROM node:24-slim

# Install system utilities
RUN apt-get update && apt-get install -y \
    git \
    ripgrep \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Configure Claude Code version via build-arg
ARG CLAUDE_VERSION=latest
RUN npm install -g "@anthropic-ai/claude-code@${CLAUDE_VERSION}"

WORKDIR /app

# Change ownership of app directory to node user
RUN chown -R node:node /app
RUN mkdir -p /home/node/.claude && \
  chown -R node:node /home/node/.claude

# Switch to node user
USER node

ENTRYPOINT ["claude"]
