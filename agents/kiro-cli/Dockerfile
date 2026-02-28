FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y git ripgrep curl iputils-ping unzip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN chown -R ubuntu:ubuntu /app
USER ubuntu
ENV PATH="/home/ubuntu/.local/bin:/home/ubuntu/.kiro/bin:${PATH}"
RUN curl -fsSL https://cli.kiro.dev/install | bash

ENTRYPOINT ["kiro-cli"]
