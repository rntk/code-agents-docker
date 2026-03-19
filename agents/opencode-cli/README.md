# OpenCode CLI (Dockerized)

This directory contains a Docker setup for running [OpenCode AI's CLI](https://opencode.ai/).

## Prerequisites

- Docker installed on your system
- An OpenCode API key (obtain from [OpenCode Console](https://console.opencode.ai/))

## Build

```bash
docker build -t opencode-cli .
```

## Run

```bash
# Set your API key as an environment variable
export OPENCODE_API_KEY="YOUR_API_KEY"

# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.opencode:/home/node/.opencode -e OPENCODE_API_KEY=$OPENCODE_API_KEY opencode-cli
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.opencode` on the host.
- Pass API keys via environment variables to avoid storing them in the image.

## Troubleshooting

- **Authentication issues**: Ensure your API key is set and the config volume is mounted correctly.
- **Permission errors**: Check that the host's `~/.opencode` directory is writable.
- **Build failures**: Verify Docker access and network for npm installs.
