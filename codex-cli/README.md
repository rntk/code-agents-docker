# Codex CLI (Dockerized)

This directory contains a Docker setup for running [OpenAI's Codex CLI](https://github.com/openai/codex).

## Prerequisites

- Docker installed on your system
- Obtain an OpenAI API key from [OpenAI Platform](https://platform.openai.com/)

## Build

```bash
docker build -t codex-cli .
```

## Run

```bash
# Set your API key as an environment variable
export OPENAI_API_KEY="YOUR_API_KEY"

# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.codex:/home/node/.codex -e OPENAI_API_KEY=$OPENAI_API_KEY codex-cli

# If already logged in, run without API key
docker run --rm -it -v $(pwd):/app -v $HOME/.codex:/home/node/.codex codex-cli

# Or authenticate via device flow
docker run --rm -it -v $(pwd):/app -v $HOME/.codex:/home/node/.codex codex-cli login --device-auth
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.codex` on the host.
- Pass API keys via environment variables or use device authentication.

## Troubleshooting

- **Authentication issues**: Ensure API key is set or complete device auth.
- **Permission errors**: Check that the host's `~/.codex` directory is writable.
- **Build failures**: Verify Docker access and network for npm installs.
