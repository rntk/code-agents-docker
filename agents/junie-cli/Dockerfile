# OCI labels for metadata
ARG VCS_REF=""
ARG BUILD_DATE=""
ARG VERSION=""

FROM ubuntu:24.04

# Install system utilities and Java (required for JetBrains tools)
RUN apt-get update && apt-get install -y \
    git \
    ripgrep \
    curl \
    iputils-ping \
    unzip \
    sed \
    && rm -rf /var/lib/apt/lists/*

# Add .local/bin to PATH for junie binary
ENV PATH="/home/ubuntu/.local/bin:${PATH}"

# Switch to ubuntu user early so install script runs as ubuntu
USER ubuntu

# Download and patch the install script, then run it as ubuntu user
# sed is temporarily used to modify the install script to workaround a 404 error due to a path issue in the original script. This should be removed once the upstream issue is resolved.
RUN curl -fsSL https://junie.jetbrains.com/install.sh | \
    sed 's/jetbrains-junie\/junie/JetBrains\/junie/g' | \
    sed 's/CHANNEL="release"/CHANNEL="nightly"/g' | \
    bash

WORKDIR /app

# Change ownership of app directory to ubuntu user (UID 1000 already exists)
USER root
RUN chown -R ubuntu:ubuntu /app
USER ubuntu

ENTRYPOINT ["junie"]
