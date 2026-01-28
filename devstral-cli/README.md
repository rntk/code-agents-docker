# Devstral CLI (Dockerized)

This directory contains a Docker setup for running [Mistral's Vibe CLI](https://mistral.ai/) (Devstral).

## Build

```bash
sudo docker build -t devstral-cli ./ --no-cache
```

## Run

```bash
sudo docker run --rm -it -v $(pwd):/app -v $HOME/.vibe:/root/.vibe -e MISTRAL_API_KEY=$MISTRAL_API_KEY --name devstral-cli devstral-cli
```

## Prerequisites

- Set your `MISTRAL_API_KEY` environment variable before running
