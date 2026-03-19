# AI Coding CLI Containers

This repository contains Dockerized setups for various AI-powered coding CLI tools, allowing you to run them in isolated containers with proper dependency management and configuration persistence.

## Included CLIs

<!-- BEGIN GENERATED INCLUDED CLIS -->
| Directory | CLI | Provider | Base Image | Non-Root |
|-----------|-----|----------|------------|-----------|
| [claude-code](./agents/claude-code/) | Claude Code | Anthropic | Node.js 24 | Yes |
| [codex-cli](./agents/codex-cli/) | Codex CLI | OpenAI | Node.js 24 | Yes |
| [copilot-cli](./agents/copilot-cli/) | Copilot CLI | GitHub | Node.js 24 | Yes |
| [codespeak](./agents/codespeak/) | CodeSpeak | Anthropic | Python 3.13 | Yes |
| [devstral-cli](./agents/devstral-cli/) | Vibe CLI | Mistral | Python 3.13 | Yes |
| [gemini-cli](./agents/gemini-cli/) | Gemini CLI | Google | Node.js 24 | Yes |
| [junie-cli](./agents/junie-cli/) | Junie CLI | JetBrains | Ubuntu 24.04 | Yes |
| [kimi-cli](./agents/kimi-cli/) | Kimi CLI | Moonshot AI | Python 3.13 | Yes |
| [kiro-cli](./agents/kiro-cli/) | Kiro CLI | AWS | Ubuntu 24.04 | Yes |
| [qwen-code](./agents/qwen-code/) | Qwen Code | Alibaba | Node.js 24 | Yes |
| [pi-coding-agent](./agents/pi-coding-agent/) | Pi Coding Agent | Mario Zechner | Node.js 24 | Yes |
<!-- END GENERATED INCLUDED CLIS -->

## Repository Structure

- `agents/`: Individual Docker environments for each AI coding CLI.
- `agents.json`: Shared metadata used by the root launcher, root README, and prompt generator.
- `scripts/sync_agents.py`: Syncs generated sections in the root README and `agent.sh` from `agents.json`.
- `generate_prompt.py`: Prompt generator that embeds the template directly and reads agent metadata from `agents.json`.
- `Makefile`: Standardized commands for building and running agents.

## Quick Start

### Using agent.sh (Recommended)

The easiest way to run or build an AI agent is with `agent.sh`:

```bash
./agent.sh run
./agent.sh build
```

This script will:
1. List all available AI agents
2. Prompt you to select one
3. Run or build the selected agent with proper volume mounts and configuration

### Using Makefile

You can also build agents using the provided Makefile from the root of the repository:

```bash
# Build all agents
make build-all

# Build a specific agent (e.g., claude-code)
make build AGENT=claude-code

# Regenerate shared metadata sections after editing agents.json
make sync-metadata
```

### Using Docker Directly

Alternatively, you can work directly with the agent directories:

```bash
# Build a specific image
docker build -t <image-name> agents/<cli-directory>

# Run it, mounting your current project to /app
docker run --rm -it -v $(pwd):/app <image-name>
```

> **Project-specific containers**: If you've generated a `Dockerfile.<agent>` for a target project using `generate_prompt.py`, use the generated prompt in that target repository and let the agent create or update the local `agent.sh` there.

## Project-Specific Dockerfiles

In addition to the base agent images, this repository includes a prompt generator for creating project-specific Dockerfile instructions for one of these agents.

### Project-Specific Dockerfile Generator

If you want to create a Dockerfile tailored for a specific software project that includes one of these AI agents, you can use the `generate_prompt.py` script. 

This tool embeds the project-specific Dockerfile template directly in the repository. It generates a comprehensive prompt that you can paste into an AI agent to produce a `Dockerfile` tailored to your target project's technology stack while pre-installing dependencies.

#### Usage

1. Run the script from the root:
   ```bash
   python3 generate_prompt.py
   ```
2. Select the agent you want to integrate from the list.
3. Copy the generated prompt.
4. Run the prompt in your target project's context using an AI agent.

## Common Features

- **Isolated environments**: Each CLI runs in its own container with required dependencies
- **Volume mounts**: Current directory mounted to `/app` for working with local code
- **Config persistence**: Authentication/config directories mounted from host home directory
- **Non-root execution**: All containers run as non-root users for security
- **Shared metadata**: Agent metadata is centralized in `agents.json`
- **Version control**: CLI versions are configurable via Docker build arguments
- **Standardized documentation**: Consistent README structure across all CLIs

## Requirements

- Docker installed on your system
- Python 3 (for the prompt generator)
- API keys for the respective services (where required)

## License

Each CLI tool maintains its own license. See the respective project documentation for details.
