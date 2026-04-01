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

# Switch to node user before installing
USER node

RUN curl -fsSL https://claude.ai/install.sh | bash

ENTRYPOINT ["claude"]
