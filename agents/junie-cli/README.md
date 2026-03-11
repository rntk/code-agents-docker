# Junie CLI (Dockerized)

This directory contains a Docker setup for running [JetBrains Junie CLI](https://www.jetbrains.com/junie/).

## Prerequisites

- Docker installed on your system
- Obtain a Junie API key from [junie.jetbrains.com/cli](https://junie.jetbrains.com/cli)

## Build

```bash
docker build -t junie-cli .
```

## Run

```bash
# Set your API key as an environment variable
export JUNIE_API_KEY="YOUR_API_KEY"

# Run the container with volume mounts for working directory and config persistence
docker run --rm -it -v $(pwd):/app -v $HOME/.junie:/home/ubuntu/.junie -e JUNIE_API_KEY=$JUNIE_API_KEY junie-cli --brave
```

## Configuration

- The container runs as a non-root user (`ubuntu`) for security.
- Mount your current directory to `/app` to work with local files.
- Config is persisted in `~/.junie` on the host.
- Pass API keys via environment variables to avoid storing them in the image.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `JUNIE_API_KEY` | **Required.** Authentication token for Junie CLI. Generate at [junie.jetbrains.com/cli](https://junie.jetbrains.com/cli). |
| `JUNIE_TASK` | Task description in plain English |
| `JUNIE_MODEL` | Model selection (optional) |
| `JUNIE_GUIDELINES_FILENAME` | Custom guidelines file path (optional) |

### Provider API Keys (BYOK - optional)

If you want to use your own API keys for specific providers:

| Variable | Description |
|----------|-------------|
| `JUNIE_ANTHROPIC_API_KEY` | API key for Anthropic (Claude models) |
| `JUNIE_OPENAI_API_KEY` | API key for OpenAI (GPT models) |
| `JUNIE_GOOGLE_API_KEY` | API key for Google AI (Gemini models) |
| `JUNIE_GROK_API_KEY` | API key for xAI (Grok models) |
| `JUNIE_OPENROUTER_API_KEY` | API key for OpenRouter |

## Troubleshooting

- **Authentication issues**: Ensure your API key is set and the config volume is mounted correctly.
- **Permission errors**: Check that the host's `~/.junie` directory is writable.
- **Build failures**: Verify Docker access and network for the install script.
