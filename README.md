# AI Coding CLI Containers

This repository contains Dockerized setups for various AI-powered coding CLI tools, allowing you to run them in isolated containers with proper dependency management and configuration persistence.

## Included CLIs

| Directory | CLI | Provider | Base Image | Non-Root |
|-----------|-----|----------|------------|-----------|
| [claude-code](./agents/claude-code/) | Claude Code | Anthropic | Node.js 24 | Yes |
| [codex-cli](./agents/codex-cli/) | Codex CLI | OpenAI | Node.js 24 | Yes |
| [copilot-cli](./agents/copilot-cli/) | Copilot CLI | GitHub | Node.js 24 | Yes |
| [devstral-cli](./agents/devstral-cli/) | Vibe CLI | Mistral | Python 3.13 | Yes |
| [gemini-cli](./agents/gemini-cli/) | Gemini CLI | Google | Node.js 24 | Yes |
| [kimi-cli](./agents/kimi-cli/) | Kimi CLI | Moonshot AI | Python 3.13 | Yes |
| [kiro-cli](./agents/kiro-cli/) | Kiro CLI | AWS | Ubuntu 24.04 | Yes |
| [qwen-code](./agents/qwen-code/) | Qwen Code | Alibaba | Node.js 24 | Yes |

## Repository Structure

- `agents/`: Individual Docker environments for each AI coding CLI.
- `skills/`: Reusable prompts and procedures (like the Dockerfile generator).
- `generate_prompt.py`: Helper script to use the `generate-project-dockerfile` skill.
- `Makefile`: Standardized commands for building and running agents.

## Quick Start

### Using run-agent.sh (Recommended)

The easiest way to run an AI agent is with the interactive `run-agent.sh` script:

```bash
./run-agent.sh
```

This script will:
1. List all available AI agents
2. Prompt you to select one (1-8)
3. Run the selected agent with proper volume mounts and configuration

### Using Makefile

You can also build and run agents using the provided Makefile from the root of the repository:

```bash
# Build all agents
make build-all

# Run a specific agent (e.g., claude-code)
make run CLI=claude-code
```

### Using Docker Directly

Alternatively, you can work directly with the agent directories:

```bash
# Build a specific image
docker build -t <image-name> agents/<cli-directory>

# Run it, mounting your current project to /app
docker run --rm -it -v $(pwd):/app <image-name>
```

## Skills & Project-Specific Dockerfiles

In addition to the base agent images, this repository includes **Skills** — specialized procedures for AI agents.

### Project-Specific Dockerfile Generator

If you want to create a Dockerfile tailored for a specific software project that includes one of these AI agents, you can use the `generate_prompt.py` script. 

This tool uses the `generate-project-dockerfile` skill to create a comprehensive prompt that you can paste into an AI agent. It will then build a `Dockerfile` specifically for your project's technology stack (Python, Node.js, Go, etc.), while pre-installing all dependencies.

#### Usage

1. Run the script from the root:
   ```bash
   python3 generate_prompt.py
   ```
2. Select the agent you want to integrate from the list.
3. Copy the generated prompt.
4. Run the prompt in your target project's context using an AI agent.

See the [skills/README.md](./skills/README.md) for more information on available skills.

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
- Python 3 (for the prompt generator)
- API keys for the respective services (where required)

## License

Each CLI tool maintains its own license. See the respective project documentation for details.
