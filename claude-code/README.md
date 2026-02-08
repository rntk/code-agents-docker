# Claude Code CLI (Dockerized)

This directory contains a Docker setup for running [Anthropic's Claude Code CLI](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview).

## Prerequisites

- Docker installed on your system
- Obtain an Anthropic API key from [Anthropic Console](https://console.anthropic.com/)

## Build

```bash
docker build -t claude-code .
```

## Run

```bash
# Set your API key as an environment variable
export ANTHROPIC_API_KEY="YOUR_API_KEY"

# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.claude:/home/node/.claude -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY claude-code --verbose --dangerously-skip-permissions
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.claude` on the host.
- Pass API keys via environment variables to avoid storing them in the image.

## Troubleshooting

- **Authentication issues**: Ensure your API key is set and the config volume is mounted correctly.
- **Permission errors**: Check that the host's `~/.claude` directory is writable.
- **Build failures**: Verify Docker access and network for npm installs.
