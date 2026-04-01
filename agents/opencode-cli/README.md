# OpenCode CLI (Dockerized)

This directory contains a Docker setup for running [OpenCode AI's CLI](https://opencode.ai/).

## Prerequisites

- Docker installed on your system
- Authentication configured (handled via `opencode login` or config file)

## Build

```bash
docker build -t opencode-cli .
```

## Run

```bash
# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.opencode:/home/node/.opencode opencode-cli
```

## Configuration

- The container runs as a non-root user for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.opencode` on the host.
- Authenticate using the CLI's built-in commands.

## Troubleshooting

- **Authentication issues**: Run `opencode login` inside the container or ensure your config is mounted correctly.
- **Permission errors**: Check that the host's `~/.opencode` directory is writable.
- **Build failures**: Verify Docker access and network for npm installs.
