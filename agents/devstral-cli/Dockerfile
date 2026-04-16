FROM python:3.13-slim

# Install system dependencies
# git: for project context
# curl: for downloading files
# ripgrep: for fast code search (grep support)
RUN apt-get update && apt-get install -y \
    git \
    curl \
    ripgrep \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install mistral-vibe
ENV PATH="/root/.local/bin:$PATH"
RUN curl -LsSf https://mistral.ai/vibe/install.sh | bash

# The container is intended to be run with a mounted volume at /app
# Example: docker run -v $(pwd):/app -v ~/.vibe:/root/.vibe -e MISTRAL_API_KEY=your_key my-mistral-vibe-image

ENTRYPOINT ["vibe"]
