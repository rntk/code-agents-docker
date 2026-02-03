# GitHub Copilot CLI (Dockerized)

This directory contains a Docker setup for running [GitHub Copilot CLI](https://github.com/cli/cli).

## Prerequisites

- Docker installed on your system
- GitHub account with Copilot access
- Authenticate via `gh auth login` (run outside container first, or mount config)

## Build

```bash
docker build -t copilot-cli .
```

## Run

```bash
# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.copilot:/home/node/.copilot copilot-cli
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.copilot` on the host.
- Authenticate using GitHub CLI before running, or mount your GitHub config.

## Troubleshooting

- **Authentication issues**: Run `gh auth login` on the host and ensure config is mounted.
- **Permission errors**: Check that the host's `~/.copilot` directory is writable.
- **Build failures**: Verify Docker access and network for npm installs.
