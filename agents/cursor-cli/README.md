# Cursor CLI (Dockerized)

This directory contains a Docker setup for running [Cursor CLI](https://cursor.com/).

## Prerequisites

- Docker installed on your system
- Obtain a Cursor account at [cursor.com](https://cursor.com)

## Build

```bash
docker build -t cursor-cli .
```

## Run

```bash
# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.cursor:/home/ubuntu/.cursor cursor-cli
```

## Configuration

- The container runs as a non-root user (`ubuntu`) for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.cursor` on the host.
- Authenticate by running `cursor-cli agent` and following the auth flow.

### Modes

| Mode   | Description |
|--------|-------------|
| `agent` | Full access to all tools (default) |
| `agent --plan` | Design approach before coding |
| `agent --mode=ask` | Read-only exploration |

## Troubleshooting

- **Authentication issues**: Run `cursor-cli agent` and authenticate via browser.
- **Permission errors**: Check that the host's `~/.cursor` directory is writable.
- **Build failures**: Verify Docker access and network for the install script.
