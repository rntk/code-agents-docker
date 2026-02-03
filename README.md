# AI Coding CLI Containers

This repository contains Dockerized setups for various AI-powered coding CLI tools, allowing you to run them in isolated containers with proper dependency management and configuration persistence.

## Included CLIs

| Directory | CLI | Provider | Base Image | Non-Root |
|-----------|-----|----------|------------|-----------|
| [claude-code](./claude-code/) | Claude Code | Anthropic | Node.js 24 | Yes |
| [codex-cli](./codex-cli/) | Codex CLI | OpenAI | Node.js 24 Alpine | Yes |
| [copilot-cli](./copilot-cli/) | Copilot CLI | GitHub | Node.js 24 | Yes |
| [devstral-cli](./devstral-cli/) | Vibe CLI | Mistral | Python 3.13 | Yes |
| [gemini-cli](./gemini-cli/) | Gemini CLI | Google | Node.js 24 | Yes |
| [kimi-cli](./kimi-cli/) | Kimi CLI | Moonshot AI | Python 3.13 | Yes |

## Quick Start

Each subdirectory contains its own Dockerfile and README with specific build and run instructions. Generally:

```bash
cd <cli-directory>
docker build -t <image-name> .
docker run --rm -it -v $(pwd):/app <image-name>
```

Alternatively, use the provided Makefile to build all images at once:

```bash
make build-all
make run CLI=<cli-name>
```

## Common Features

- **Isolated environments**: Each CLI runs in its own container with required dependencies
- **Volume mounts**: Current directory mounted to `/app` for working with local code
- **Config persistence**: Authentication/config directories mounted from host home directory
- **Non-root execution**: All containers run as non-root users for security
- **Optimized builds**: Uses `.dockerignore` to exclude unnecessary files
- **Version control**: CLI versions are configurable via Docker build arguments
- **Standardized documentation**: Consistent README structure across all CLIs

## Requirements

- Docker installed on your system
- API keys for the respective services (where required)

## License

Each CLI tool maintains its own license. See the respective project documentation for details.
