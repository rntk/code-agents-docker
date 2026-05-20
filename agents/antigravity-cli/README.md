# Antigravity CLI (Dockerized)

This directory contains a Docker setup for running [Antigravity CLI](https://antigravity.google).

## Prerequisites

- Docker installed on your system
- Obtain an Antigravity account or credentials if required

## Build

```bash
docker build -t antigravity-cli .
```

## Run

```bash
# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.gemini:/home/ubuntu/.gemini antigravity-cli
```

## Configuration

- The container runs as a non-root user (`ubuntu`) for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.gemini` on the host.
- Authenticate by running the CLI and following any authentication flow.

## Troubleshooting

- **Permission errors**: Check that the host's `~/.gemini` directory is writable.
- **Build failures**: Verify Docker access and network for the install script.
