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
RUN mkdir -p /home/node/.npm-global && \
    chown -R node:node /home/node/.npm-global

# Set npm global prefix to user-writable directory
ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
ENV PATH="/home/node/.npm-global/bin:${PATH}"

# Switch to non-root user for security
USER node

# Configure Gemini CLI version via build-arg
ARG GEMINI_VERSION=latest
RUN npm install -g "@google/gemini-cli@${GEMINI_VERSION}"

ENTRYPOINT ["gemini"]
