# Kiro CLI (Dockerized)

This directory contains a Docker setup for running [Kiro CLI](https://kiro.dev/docs/cli/installation/).

## Prerequisites

- Docker installed on your system
- A Kiro account

## Build

```bash
docker build -t kiro-cli .
```

## To login
```bash
docker run --rm -it \
  -v $(pwd):/app \
  -v $HOME/.kiro:/home/ubuntu/.kiro \
  -v $HOME/.local/share/kiro-cli:/home/ubuntu/.local/share/kiro-cli \
  kiro-cli login --use-device-flow 
```

## Run

```bash
# Run the container with volume mount for working directory
docker run --rm -it -v $(pwd):/app kiro-cli --trust-all-tools
```

To persist authentication and data:

```bash
docker run --rm -it \
  -v $(pwd):/app \
  -v $HOME/.kiro:/home/ubuntu/.kiro \
  -v $HOME/.local/share/kiro-cli:/home/ubuntu/.local/share/kiro-cli \
  kiro-cli --trust-all-tools
```

## Configuration

- The container runs as a non-root user `ubuntu` for security.
- Mount your current directory to `/app` to work with local files.
- The agent is installed via the official `.deb` package on an Ubuntu 24.04 base.

## Troubleshooting

- **Browser Authentication**: Since the CLI runs in Docker, the browser redirect might not work automatically if it tries to open a local browser. You may need to copy the URL from the terminal and open it manually.
- **Permission errors**: Ensure the mounted volume allows write access.
- **Build failures**: Check Docker is running and you have internet access to download the AppImage.
