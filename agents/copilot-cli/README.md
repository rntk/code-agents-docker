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
# Authenticate once in the container
docker run --rm -it -v $(pwd):/app -v $HOME/.copilot:/home/node/.copilot copilot-cli login

# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.copilot:/home/node/.copilot copilot-cli --allow-all

# For non-interactive/container-first setups, GitHub recommends auth via env vars
docker run --rm -it \
  -v $(pwd):/app \
  -v $HOME/.copilot:/home/node/.copilot \
  -e COPILOT_GITHUB_TOKEN=$COPILOT_GITHUB_TOKEN \
  copilot-cli --allow-all
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.copilot` on the host.
- Prefer `copilot login` for interactive auth inside the container.
- For headless or automated use, prefer environment variables such as `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, or `GITHUB_TOKEN`.
- GitHub CLI (`gh`) can also be used as a fallback auth source, but it is not required by this image.

## Troubleshooting

- **Authentication issues**: Re-run `copilot login` in the container or provide a supported token env var.
- **Permission errors**: Check that the host's `~/.copilot` directory is writable.
- **Build failures**: Verify Docker access and network for npm installs.
