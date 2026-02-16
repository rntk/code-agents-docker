# Qwen Code CLI (Dockerized)

This directory contains a Docker setup for running [Qwen Code CLI](https://qwen.ai).

## Prerequisites

- Docker installed on your system
- Qwen Code configuration or credentials (usually handled via `qwen login` or similar)

## Build

```bash
docker build -t qwen-code .
```

## Run

```bash
# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.qwen:/home/node/.qwen qwen-code --yolo
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.qwen` on the host.
