# Kimi CLI (Dockerized)

This directory contains a Docker setup for running [Kimi Code CLI](https://kimi.com/).

## Prerequisites

- Docker installed on your system
- Kimi account (authentication handled within the CLI)

## Build

```bash
docker build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -t kimi-cli .
```

## Run

```bash
# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.kimi:/home/appuser/.kimi kimi-cli
```

## Configuration

- The container runs as a non-root user with UID/GID matching the host for file permission compatibility.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.kimi` on the host.
- Authenticate using the CLI's built-in commands.

## Troubleshooting

- **UID/GID issues**: Ensure build args match your host user (`id -u` and `id -g`).
- **Permission errors**: Check that the host's `~/.kimi` directory is writable.
- **Build failures**: Verify Docker access and network for apt/pip installs.
