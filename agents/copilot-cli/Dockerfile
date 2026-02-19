FROM node:24-slim

# Install system utilities
RUN apt-get update && apt-get install -y \
    git \
    ripgrep \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Configure Copilot CLI version via build-arg
ARG COPILOT_VERSION=latest
RUN npm install -g "@github/copilot@${COPILOT_VERSION}"

WORKDIR /app

# Change ownership of app directory to node user
RUN chown -R node:node /app
RUN mkdir -p /home/node/.copilot && \
  chown -R node:node /home/node/.copilot

# Switch to node user
USER node

ENTRYPOINT ["copilot"]
