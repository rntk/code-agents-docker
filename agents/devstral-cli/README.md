# Devstral CLI (Dockerized)

This directory contains a Docker setup for running [Mistral's Vibe CLI](https://mistral.ai/) (Devstral).

## Prerequisites

- Docker installed on your system
- Obtain a Mistral API key from [Mistral Console](https://console.mistral.ai/)

## Build

```bash
docker build -t devstral-cli .
```

## Run

```bash
# Set your API key as an environment variable
export MISTRAL_API_KEY="YOUR_API_KEY"

# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.vibe:/home/appuser/.vibe -e MISTRAL_API_KEY=$MISTRAL_API_KEY devstral-cli
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.vibe` on the host (mapped to `/home/appuser/.vibe` in container).
- Pass API keys via environment variables to avoid storing them in the image.

## Troubleshooting

- **API key issues**: Ensure `MISTRAL_API_KEY` is set correctly.
- **Permission errors**: Check that the host's `~/.vibe` directory is writable.
- **Build failures**: Verify Docker access and network for pip/uv installs.
