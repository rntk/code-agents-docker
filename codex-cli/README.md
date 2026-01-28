# Codex CLI (Dockerized)

This directory contains a Docker setup for running [OpenAI's Codex CLI](https://github.com/openai/codex).

## Build

```bash
sudo docker build -t codex-cli --no-cache .
```

## Run

```bash
# Run with API key
sudo docker run --rm -it -v "$HOME/.codex":/home/node/.codex -v $(pwd):/app -e OPENAI_API_KEY=$OPENAI_API_KEY --name codex-cli codex-cli

# Or login with device authentication
sudo docker run --rm -it -v "$HOME/.codex":/home/node/.codex -v $(pwd):/app --name codex-cli codex-cli login --device-auth
```
