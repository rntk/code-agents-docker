# Pi Coding Agent (Dockerized)

This directory contains a Docker setup for running [Mario Zechner's Pi Coding Agent](https://github.com/mariozechner/pi-coding-agent).

## Prerequisites

- Docker installed on your system
- No API key required (authentication handled via config file)

## Build

```bash
docker build -t pi-coding-agent .
```

Or with a specific version:

```bash
docker build --build-arg PI_VERSION=1.0.0 -t pi-coding-agent .
```

## Run

```bash
# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v "$(pwd):/app" -v "$HOME/.pi:/home/node/.pi" pi-coding-agent
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.pi` on the host.

## Troubleshooting

- **Installation issues**: Ensure the package `@mariozechner/pi-coding-agent` is available on npm.
- **Permission errors**: Check that the host's `~/.pi` directory is writable.
- **Build failures**: Verify Docker access and network for npm installs.
