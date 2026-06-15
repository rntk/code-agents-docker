# Grok CLI (Dockerized)

This directory contains a Docker setup for running [Grok CLI](https://x.ai/cli) from xAI.

## Prerequisites

- Docker installed on your system
- A Grok API key or deployment key from [xAI](https://x.ai)

## Build

```bash
docker build -t grok-build-cli .
```

## Run

```bash
# Run with API key authentication (non-browser environments)
export XAI_API_KEY="xai-..."

# Run the container with volume mounts for working directory and config persistence
docker run --rm -it \
  -v $(pwd):/app \
  -v $HOME/.grok:/home/ubuntu/.grok \
  -v $HOME/.agents:/home/ubuntu/.agents \
  -e XAI_API_KEY=$XAI_API_KEY \
  grok-build-cli
```

## Configuration

- The container runs as a non-root user (`ubuntu`) for security.
- Mount your current directory to `/app` to work with local files.
- Config and authentication are persisted in `~/.grok` on the host.
- User-level skills/commands from `~/.agents/skills/` and `~/.agents/commands/` are mounted from the host.
- Project-local `.grok/` and `.agents/` directories are discovered automatically via the `/app` mount.
- Pass `XAI_API_KEY` via environment variable, or run `grok login` inside the container to create `~/.grok/auth.json`.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `XAI_API_KEY` | **Recommended.** API key for Grok authentication in non-browser environments. |
| `GROK_CHANNEL` | Release channel (`stable`, `alpha`, `enterprise`; default: `stable`). |
| `GROK_PROXY_URL` | Custom proxy URL for deployment config fetching. |

## Troubleshooting

- **Authentication issues**: Ensure `XAI_API_KEY` is set, or `~/.grok/auth.json` is mounted correctly.
- **Permission errors**: Check that the host's `~/.grok` and `~/.agents` directories are writable.
- **Build failures**: Verify Docker access and network connectivity for the install script.
