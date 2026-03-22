# AGENTS.md

## Project Overview

AI Coding CLI Containers — Dockerized environments for 12 AI-powered coding CLI tools (Claude Code, Codex CLI, Gemini CLI, etc.). Each agent runs in an isolated container with proper dependency management and config persistence.

## Repository Structure

```
/app
├── agents/<name>/        # Per-agent: Dockerfile + README.md (exactly 2 files each)
├── agents.json           # Single source of truth for all agent metadata
├── agent.sh              # Interactive menu script (run/build/update agents)
├── scripts/
│   ├── make.py           # Build/sync/clean CLI (replaces Makefile)
│   ├── sync_agents.py    # Syncs agents.json → agent.sh and README.md
│   └── generate_prompt.py # Prompt generator for project-specific Dockerfiles
├── AGENTS.md             # This file
└── README.md             # Root docs (sections auto-generated from agents.json)
```

## Build & Test Commands

```bash
# Build all agent images (iterates agents/*/Dockerfile)
python3 scripts/make.py build-all

# Build a single agent image
python3 scripts/make.py build claude-code   # builds agents/claude-code/Dockerfile

# Run an agent interactively (interactive menu)
./agent.sh run                              # or: python3 scripts/make.py run

# Update an agent's CLI in-place (root shell → commit)
./agent.sh update

# Sync generated sections in agent.sh and README.md from agents.json
python3 scripts/make.py sync-metadata       # runs: python3 scripts/sync_agents.py

# Generate a project-specific Dockerfile prompt (interactive)
python3 scripts/make.py generate-prompt     # or: python3 scripts/generate_prompt.py -o prompt.md

# Clean dangling Docker images
python3 scripts/make.py clean

# Validate a Python script parses cleanly (no formal linter configured)
python3 scripts/sync_agents.py              # also runs the sync
python3 scripts/generate_prompt.py          # will error on parse issues
```

There is no test suite. Validation is done by `sync_agents.py` which checks agent IDs (`^[a-z0-9-]+$`), image dir paths (`^agents/[a-z0-9-]+$`), and env var names (`^[A-Z_][A-Z0-9_]*$`) before writing.

## Code Style

### Python (`scripts/make.py`, `scripts/sync_agents.py`, `scripts/generate_prompt.py`)

- **Shebang**: `#!/usr/bin/env python3` on first line
- **Imports**: stdlib only, one per line, grouped: stdlib first then blank line before local imports. Use `from pathlib import Path` style for path operations.
- **Path handling**: Use `pathlib.Path` for filesystem paths (`sync_agents.py`); `os.path` is also acceptable (`generate_prompt.py`) — match the existing file you're editing.
- **Functions**: snake_case, no type annotations in existing code. Use docstring-style comments sparingly only when non-obvious.
- **Error handling**: Raise `ValueError` with descriptive messages. Use `sys.exit(1)` for fatal user-facing errors. Use `try/except` for expected failures (e.g., `FileNotFoundError`, `ValueError` on user input).
- **String formatting**: f-strings exclusively. Use `shlex.quote()` for shell-unsafe strings.
- **Constants**: UPPER_SNAKE_CASE at module level (e.g., `ROOT`, `MANIFEST_PATH`, `PROMPT_TEMPLATE`).
- **Entry point**: `if __name__ == "__main__": main()`
- **File I/O**: Context managers (`with open(...) as f`). Prefer `Path.read_text()`/`Path.write_text()` when using pathlib.
- **Long strings**: Multi-line via triple-quoted constants (`PROMPT_TEMPLATE`), not string concatenation.
- **No type hints or linters** are configured; keep code clean but don't add annotations not already present.
- **Data flow**: `agents.json` → `sync_agents.py` → `agent.sh` + `README.md`. The sync script is the bridge; never skip it.

### Bash (`agent.sh`)

- **Shebang**: `#!/bin/bash`
- **Functions**: `name() { ... }` style (no `function` keyword). Use `run_agent`, `build_agent`, `update_agent`, `usage`.
- **Dispatch**: Top-level `case "$1" in` dispatches to functions.
- **Generated sections**: Wrapped in `# BEGIN/END GENERATED <SECTION>` markers — never edit manually, always use `sync_agents.py`.
- **Variable quoting**: Always double-quote variables (`"$choice"`, `"$IMAGE"`). Use `"$(pwd)"` for command substitution.
- **User prompts**: `read -rp "prompt text: " variable`
- **Docker commands**: Wrapped in `execute` helper that logs the command before running it.
- **Color output**: Use ANSI escapes in `execute()` (e.g., `\033[1;34m`).
- **Container naming**: Use `"update-${IMAGE%%:*}-$$"` pattern for unique container names.
- **Case branches**: Each agent gets its own numbered case branch; invalid selections exit 1.

### Dockerfiles (`agents/<name>/Dockerfile`)

- **Base images**: `node:24-slim` (npm CLIs), `python:3.13-slim` (uv/pip CLIs), `ubuntu:24.04` (binary CLIs)
- **Layer ordering** (least to most changing): OCI labels → FROM → apt-get system packages → env setup → user creation → CLI install → ENTRYPOINT
- **System packages**: Single `apt-get update && apt-get install -y ... && rm -rf /var/lib/apt/lists/*` block. Always include: `git`, `ripgrep`, `curl`, `iputils-ping`.
- **Non-root user**: Always drop privileges via `USER` before installing CLI. Use existing image users (`node`, `ubuntu`) or create one (`useradd -m -s /bin/bash`).
- **Version pinning**: `ARG <NAME>_VERSION=latest` then use in install command.
- **npm install**: Set `NPM_CONFIG_PREFIX` to user-writable dir; use `ENV PATH` to include it.
- **uv install**: `COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/` then `uv tool install <pkg>`.
- **Entrypoint**: `ENTRYPOINT ["command"]` — no CMD, no EXPOSE (unless agent-specific).
- **Comments**: Brief comments above key blocks (e.g., `# Install system utilities`, `# Switch to non-root user`).
- **OCI labels**: Optional `ARG VCS_REF`, `ARG BUILD_DATE`, `ARG VERSION` at the top of the file.

### JSON (`agents.json`)

- 2-space indentation. Each agent has: `id`, `display_name`, `provider`, `base_image`, `non_root`, `image_dir`, `entrypoint`, `config_dir_host`, `config_path_container`, `docs_url`, `update_hint`, `run` (with `mounts`, `env_vars`, `docker_args`, `command_args`).
- Agent IDs are lowercase kebab-case matching `^[a-z0-9][a-z0-9-]*$`.

## Adding a New Agent

1. Create `agents/<name>/Dockerfile` and `agents/<name>/README.md`
2. Add metadata entry to `agents.json` (all fields listed above)
3. Run `python3 scripts/make.py sync-metadata` to regenerate `agent.sh` and `README.md` generated sections
4. Verify: `python3 scripts/make.py build <name>`

Agent naming: use lowercase kebab-case (e.g., `my-new-cli`). The `id` field in `agents.json` must match the directory name under `agents/`.

Dockerfile checklist for new agents:
- Pick the right base image for the CLI's language runtime
- Install `git`, `ripgrep`, `curl`, `iputils-ping` in the apt-get block
- Create or use a non-root user before CLI installation
- Pin the CLI version via `ARG` (default `latest`)
- Set `ENTRYPOINT` to the CLI command
- Avoid `EXPOSE` and `CMD` unless agent-specific

## Generated Sections

`sync_agents.py` replaces content between marker pairs. Never hand-edit these sections.

- `README.md`: `<!-- BEGIN/END GENERATED INCLUDED CLIS -->` — markdown table of all agents
- `agent.sh`: `# BEGIN/END GENERATED RUN MENU` — numbered agent list for run command
- `agent.sh`: `# BEGIN/END GENERATED RUN CASE` — `docker run` invocations per agent
- `agent.sh`: `# BEGIN/END GENERATED UPDATE MENU` — numbered list for update command
- `agent.sh`: `# BEGIN/END GENERATED UPDATE CASE` — `IMAGE` and `HINT` variables per agent
- `agent.sh`: `# BEGIN/END GENERATED BUILD MENU` — numbered list for build command
- `agent.sh`: `# BEGIN/END GENERATED BUILD CASE` — `docker build` commands per agent
- `agent.sh`: `# BEGIN/END GENERATED AGENT COUNT` — total agent count variable

Only edit the manual boilerplate in `agent.sh`: the `execute()` helper, the `usage()` function, the top-level `case "$1" in` dispatch, and `update_agent()` logic (container name, commit steps).

## Key Conventions

- Generated sections in `agent.sh` and `README.md` must never be edited manually — always use `python3 scripts/make.py sync-metadata`
- Project working directory is mounted at `/app` in all containers
- Agent config dirs mounted from `$HOME/.<config_dir>` on host
- All containers run as non-root users (security best practice)
- No test framework exists; validation is the JSON schema checks in `sync_agents.py`
- No Cursor rules (`.cursor/rules/`), Copilot instructions (`.github/copilot-instructions.md`), or `.cursorrules` exist
- When modifying `agent.sh`, only edit manual boilerplate — generated sections are overwritten by `sync_agents.py`
- Always run `python3 scripts/make.py sync-metadata` after editing `agents.json` to keep all files in sync
