# Skills

Reusable prompts and procedures for AI coding agents to perform specialized tasks.

## Available Skills

### generate-project-dockerfile

Analyzes a target software project and generates a project-specific Dockerfile that extends one of the base AI coding CLI images with all required runtimes, tools, and dependencies.

**Use case**: The base Dockerfiles in this repo provide general-purpose containers for each CLI agent. But real projects need additional tools — a Python project needs `pytest` to run tests, a Node.js project using a Go backend needs the Go runtime, etc. This skill bridges that gap.

**How it works**:

1. Reads the reference Dockerfile for the chosen CLI agent (to learn how it's installed)
2. Checks if the target project has its own Dockerfile — if so, uses it as the base (Strategy A)
3. If no project Dockerfile exists, uses `ubuntu:24.04` as a universal base (Strategy B)
4. Scans the target project to detect languages, frameworks, testing tools, build systems, and system dependencies
5. Generates a tailored Dockerfile that combines the project's environment with the AI coding agent
6. Outputs the Dockerfile and a companion README with build/run instructions

**Inputs**:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `PROJECT_DIR` | Path to the project to analyze | `/home/user/my-web-app` |
| `CLI_AGENT` | Which AI coding CLI to use | `claude-code` |
| `DOCKERFILES_REPO` | Path to this repository | `/home/user/ai-coding-cli-containers` |

**Prompt file**: [`generate-project-dockerfile/prompt.md`](./generate-project-dockerfile/prompt.md)

### Usage

Feed the prompt to your AI coding agent along with the three input parameters. For example, with Claude Code:

```bash
# Point the agent at your project
claude "Follow the skill instructions in /path/to/skills/generate-project-dockerfile/prompt.md. \
  PROJECT_DIR=/home/user/my-django-app \
  CLI_AGENT=claude-code \
  DOCKERFILES_REPO=/path/to/ai-coding-cli-containers"
```

The agent will analyze the project, detect requirements, and generate:
- `{CLI_AGENT}/Dockerfile.{project_name}` — the project-specific Dockerfile
- `{CLI_AGENT}/README.{project_name}.md` — build/run instructions and detected stack summary
