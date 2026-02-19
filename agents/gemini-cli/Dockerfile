FROM node:24-slim

# Install system utilities
RUN apt-get update && apt-get install -y \
    git \
    ripgrep \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Configure Gemini CLI version via build-arg
ARG GEMINI_VERSION=latest
RUN npm install -g "@google/gemini-cli@${GEMINI_VERSION}"

WORKDIR /app

# Switch to non-root user for security
USER node

ENTRYPOINT ["gemini"]
