# Claude Code CLI (Dockerized)

This directory contains a Docker setup for running [Anthropic's Claude Code CLI](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview).

## Build

```bash
sudo docker build -t claude-code ./ --no-cache
```

## Run

```bash
# Run with volume mount for Claude authentication persistence
sudo docker run --rm -it -v $(pwd):/app -v $HOME/.claude:/home/node/.claude --name claude-code claude-code
```
