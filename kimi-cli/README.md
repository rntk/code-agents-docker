# Kimi CLI (Dockerized)

This directory contains a Docker setup for running [Kimi Code CLI](https://kimi.com/).

## Build

```bash
docker build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -t kimi-cli .
```

## Run

```bash
docker run -it -v ~/.kimi:/home/appuser/.kimi -v $(pwd):/app kimi-cli
```

## Features

- Runs as non-root user with configurable UID/GID matching the host user
- Preserves Kimi configuration via volume mount to `~/.kimi`
