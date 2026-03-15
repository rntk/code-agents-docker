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

WORKDIR /app
RUN chown -R node:node /app
RUN mkdir -p /home/node/.qwen /home/node/.npm-global && \
    chown -R node:node /home/node/.qwen /home/node/.npm-global

# Set npm global prefix to user-writable directory
ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
ENV PATH="/home/node/.npm-global/bin:${PATH}"

# Switch to node user before installing
USER node

# Configure Qwen Code version via build-arg
ARG QWEN_VERSION=latest
RUN npm install -g "@qwen-code/qwen-code@${QWEN_VERSION}"

ENTRYPOINT ["qwen"]
