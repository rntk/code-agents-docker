# Qwen Code CLI (Dockerized)

This directory contains a Docker setup for running [Qwen Code CLI](https://qwen.ai).

## Prerequisites

- Docker installed on your system
- Qwen Code credentials (configured via `qwen login` or config file)

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
- Authenticate using the CLI's built-in login commands.

## Troubleshooting

- **Authentication issues**: Run `qwen login` inside the container or ensure your config is mounted correctly.
- **Permission errors**: Check that the host's `~/.qwen` directory is writable.
- **Build failures**: Verify Docker access and network for npm installs.
