# GitHub Copilot CLI (Dockerized)

This directory contains a Docker setup for running [GitHub Copilot CLI](https://github.com/cli/cli).

## Build

```bash
sudo docker build -t copilot ./ --no-cache
```

## Run

```bash
sudo docker run --rm -it -v $(pwd):/app -v $HOME/.copilot:/home/node/.copilot --name copilot copilot
```
