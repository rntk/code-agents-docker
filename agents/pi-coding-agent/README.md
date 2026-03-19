# Pi Coding Agent (Dockerized)

This directory contains a Docker setup for running [Mario Zechner's Pi Coding Agent](https://github.com/mariozechner/pi-coding-agent).

## Prerequisites

- Docker installed on your system
- Required API key or authentication credentials (if applicable)

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
# Basic run with volume mounts
docker run --rm -it -v "$(pwd):/app" -v "$HOME/.pi:/home/node/.pi" pi-coding-agent
```

With environment variables (if required):

```bash
# Set any required API keys as environment variables
export PI_API_KEY="YOUR_API_KEY"

# Run the container
docker run --rm -it -v "$(pwd):/app" -v "$HOME/.pi:/home/node/.pi" -e PI_API_KEY="$PI_API_KEY" pi-coding-agent
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.pi` on the host.
- Pass API keys or credentials via environment variables to avoid storing them in the image.

## Troubleshooting

- **Installation issues**: Ensure the package `@mariozechner/pi-coding-agent` is available on npm.
- **Permission errors**: Check that the host's `~/.pi` directory is writable.
- **Build failures**: Verify Docker access and network for npm installs.
