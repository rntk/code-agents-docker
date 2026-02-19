FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y wget git ripgrep curl iputils-ping && \
    wget https://desktop-release.q.us-east-1.amazonaws.com/latest/kiro-cli.deb && \
    dpkg -i kiro-cli.deb || true && \
    apt-get install -f -y && \
    rm kiro-cli.deb && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN chown -R ubuntu:ubuntu /app
USER ubuntu

ENTRYPOINT ["kiro-cli"]
