# GitHub Copilot CLI (Dockerized)

This directory contains a Docker setup for running [GitHub Copilot CLI](https://github.com/features/copilot/cli).

## Prerequisites

- Docker installed on your system
- GitHub account with Copilot access

## Build

```bash
docker build -t copilot-cli .
```

## Run

```bash
# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.copilot:/home/node/.copilot copilot-cli --allow-all
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.copilot` on the host.
- Authenticate using GitHub CLI before running, or mount your GitHub config.

## Troubleshooting

- **Permission errors**: Check that the host's `~/.copilot` directory is writable.
- **Build failures**: Verify Docker access and network for npm installs.
