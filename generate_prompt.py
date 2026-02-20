#!/usr/bin/env python3
import os
import sys

# Per-agent metadata used by the prompt template.
# Keep this explicit so command/config assumptions don't drift for irregular names.
AGENT_METADATA = {
    "claude-code": {"entrypoint": "claude", "config_dir": "claude"},
    "codex-cli": {"entrypoint": "codex", "config_dir": "codex"},
    "copilot-cli": {"entrypoint": "copilot", "config_dir": "copilot"},
    "devstral-cli": {"entrypoint": "vibe", "config_dir": "vibe"},
    "gemini-cli": {"entrypoint": "gemini", "config_dir": "gemini"},
    "kimi-cli": {"entrypoint": "kimi", "config_dir": "kimi"},
    "kiro-cli": {"entrypoint": "kiro-cli", "config_dir": "kiro"},
    "qwen-code": {"entrypoint": "qwen", "config_dir": "qwen"},
}

# The base prompt template from skills/generate-project-dockerfile/prompt.md
# Updated to refer to embedded content and improved for use with agents.
PROMPT_TEMPLATE = """# Skill: Generate Project-Specific Dockerfile and Bash Script

You are a DevOps engineer specializing in containerized development environments for AI coding agents.

## Objective

Generate a project-specific Dockerfile and a companion bash script that gives an AI coding CLI agent everything it needs to work on a given software project.

**Strategy:**
1. **If the project has its own Dockerfile** — extend it by adding the coding agent (Strategy A - preferred)
2. **If the project has no Dockerfile** — choose an appropriate base image, install runtimes and tools, then add the coding agent (Strategy B)

**The generated Dockerfile must pre-install all project dependencies** so the environment is ready for testing and execution immediately.

**The generated bash script (`agent.sh`) is a single unified script** that manages all agents. It must be created if missing, or updated to add/modify the entry for the current agent while keeping all other agents intact.

## Inputs

Name of the AI coding CLI: {CLI_AGENT}

---

### Step 1: Reference Information

Below is the **Reference Dockerfile** and **Reference README.md** for the {CLI_AGENT} agent. 
Extract the following from these files:
- CLI installation method (e.g., `npm install -g @anthropic-ai/claude-code`)
- Required runtime (Node.js, Python, etc.)
- Entrypoint command (e.g., `claude`, `codex`, `gemini`)
- Config directories (e.g., `/home/node/.claude`)
- Build ARGs for version pinning
- Run examples and required parameters (e.g., mounting config directories, environment variables, command-line flags)

#### Reference Dockerfile:
```dockerfile
{DOCKERFILE_CONTENT}
```

#### Reference README.md:
```markdown
{README_CONTENT}
```

---

### Step 2: Analyze the Target Project

Detect the project's technology stack by scanning for:

**Languages & Package Managers:**
- Python: `*.py`, `pyproject.toml`, `requirements.txt`, `Pipfile` → pip/poetry/uv
- Node.js: `*.js`, `package.json`, `*lock*` files → npm/yarn/pnpm
- Go: `*.go`, `go.mod` → go modules
- Rust: `*.rs`, `Cargo.toml` → cargo
- Java: `*.java`, `pom.xml`, `build.gradle` → maven/gradle
- Ruby: `*.rb`, `Gemfile` → bundler
- PHP: `*.php`, `composer.json` → composer
- C/C++: `*.c`, `*.cpp`, `Makefile`, `CMakeLists.txt` → make/cmake

**Testing & Quality Tools:**
Check dependencies for: pytest, jest, mocha, eslint, ruff, mypy, golangci-lint, clippy, etc.

**System Dependencies:**
Common needs: `libpq-dev` (PostgreSQL), `libmysqlclient-dev` (MySQL), `build-essential`, `libjpeg`, `libpng`, `ffmpeg`, `libxml2-dev`

---

### Step 3: Choose the Base Image Strategy

**Strategy A: Project Has Its Own Dockerfile (Preferred)**

Use when: Project contains `Dockerfile`, `Dockerfile.dev`, or `docker-compose.yml` with build context.

Approach:
1. Read the project's Dockerfile - understand base image, packages, user setup
2. Reproduce the project's environment (base, system deps, project dependencies)
3. Add CLI agent installation and required runtime if missing
4. Set CLI agent as `ENTRYPOINT`
5. Add non-root user if missing
6. Remove `EXPOSE` and app-specific `CMD`
7. For multi-stage builds, base on final stage but include dev dependencies

**Strategy B: No Project Dockerfile**

Use when: No Dockerfile exists or it's unsuitable (scratch/distroless images).

Base image selection:
1. Primary runtime has slim image? → Use it (e.g., `node:20-slim`, `python:3.13-slim`)
2. Multiple runtimes/complex deps? → Use `ubuntu:24.04`
3. Alpine only if dependencies are musl-compatible

Approach:
1. Start from chosen base
2. Install language runtimes (via distro packages or verified binaries with checksum validation)
3. Install CLI agent
4. Install only required global dev tools
5. Set up non-root user

**Runtime Installation (Ubuntu):**
- Node.js: distro package or official image (avoid `curl | bash`)
- Python: `apt-get install python3 python3-pip python3-venv`
- Go: Download tarball with checksum verification, support multi-arch via `$TARGETARCH`
- Rust: rustup with checksum, as non-root user
- Ruby: `apt-get install ruby-full`
- Java: `apt-get install openjdk-21-jdk`

**Multi-platform Support:**
Use `ARG TARGETARCH` and case statements for platform-specific downloads. Support amd64 and arm64.

```dockerfile
ARG TARGETARCH
RUN case "$TARGETARCH" in \\
      amd64) ARCH='amd64' ;; \\
      arm64) ARCH='arm64' ;; \\
      *) echo "Unsupported: $TARGETARCH" && exit 1 ;; \\
    esac && \\
    curl -fsSLO "https://example.com/tool-${{ARCH}}.tar.gz" && \\
    curl -fsSLO "https://example.com/tool-${{ARCH}}.tar.gz.sha256" && \\
    sha256sum -c "tool-${{ARCH}}.tar.gz.sha256"
```

---

### Step 4: Generate the Dockerfile

**Core Requirements:**

1. **Layer ordering** (least to most frequently changing): System packages → Language runtimes → Project dependencies → CLI agent → Global tools → User setup → Entrypoint

2. **System packages**: Install early, group `apt-get` commands, clean up: `&& rm -rf /var/lib/apt/lists/*`

3. **Project dependencies**: MUST `COPY` manifest files + `RUN` install commands (e.g., `COPY package.json ./ && RUN npm install`)

4. **Global tools**: Install sparingly, only if not project-managed. Version-pin when possible.

5. **Non-root user**: Always create `appuser` (UID 1000) if missing

6. **Entrypoint**: Set to CLI agent command (e.g., `ENTRYPOINT ["{CLI_AGENT_NAME_LOWER}"]`)

7. **Source code**: Optional `COPY . .` after dependency install. Agent typically volume-mounts at runtime.

8. **Header comment**: Include generated-for project name, strategy used, base image, and detected tech stack

**Output:**
- Save as `Dockerfile.{CLI_AGENT}` in the current project directory
- Add brief build/run instructions as comments at the top of the Dockerfile. Include the generated-for project name, strategy used, base image, detected tech stack, required environment variables, and complete run examples from the agent-specific README (e.g., mounting config directories, command-line parameters like `-a never` for codex-cli).

**Must Include:**
- Strategy choice (A/B) and rationale
- CLI version ARG (default: `latest`)
- Non-root user, `/app` workdir
- Cache cleanup after package installs
- Project dependency installation
- No `curl | bash` without checksums

---

### Step 5: Create or Update the Unified Agent Runner Script (`agent.sh`)

Instead of creating a per-agent script, maintain a single `agent.sh` that manages all agents.
The current agent to add/update is: **{CLI_AGENT}**

**Reference `agent.sh`** (current contents — study the existing entries to understand numbering and style):
```bash
{RUN_AGENT_SCRIPT_CONTENT}
```

#### Target structure

`agent.sh` must use the following structure with separate `run_agent` and `build_agent` functions and a top-level subcommand dispatch:

```bash
#!/bin/bash

run_agent() {{
    echo "Available AI Agents:"
    echo "1. <agent-1>"
    # ... one line per agent ...
    read -rp "Select agent (1-N): " choice
    case "$choice" in
        1) sudo docker run --rm -it -v "$(pwd):/app" \
               <VOLUME_MOUNTS> <ENV_VARS> <agent-1>:latest <FLAGS> ;;
        # ... one branch per agent ...
        *) echo "Invalid selection" ; exit 1 ;;
    esac
}}

build_agent() {{
    echo "Available AI Agents:"
    echo "1. <agent-1>"
    # ... one line per agent ...
    read -rp "Select agent to build (1-N): " choice
    case "$choice" in
        1) docker build --no-cache -f Dockerfile.<agent-1> -t <agent-1>:latest . ;;
        # ... one branch per agent ...
        *) echo "Unknown agent" ; exit 1 ;;
    esac
}}

usage() {{
    echo "Usage: $0 <run|build> [args...]"
    echo ""
    echo "Commands:"
    echo "  run    Select and run an agent container (default)"
    echo "  build  Build an agent Docker image"
    exit 1
}}

case "$1" in
    run|"")  run_agent ;;
    build)   build_agent ;;
    *)       usage ;;
esac
```

#### If `agent.sh` already exists:

1. **Detect structure**: Check whether the file already has the `run_agent()`/`build_agent()` function layout above.
   - If it only has a flat `case "$choice" in` with no subcommand dispatch (like the reference above), **refactor** it: wrap the existing run logic inside a `run_agent()` function, add a `build_agent()` function, add `usage()`, and add the top-level `case "$1" in` dispatch. Preserve all existing `docker run` lines verbatim.
   - If it already has the target structure, proceed directly to adding/updating entries.

2. **Determine the entry number**: Count existing `echo "N. <agent>"` lines inside `run_agent` to find the highest N. The new entry uses N+1 as its number. Apply the same number consistently in the `echo` menu line, the `read -rp` range hint, and the `case` branch — in both `run_agent` and `build_agent`.

3. **Add or update `{CLI_AGENT}`**:
   - In `run_agent`: check if `{CLI_AGENT}` already has a `case` branch.
     - If present: replace only that `docker run` line.
     - If absent: append `echo "N+1. {CLI_AGENT}"` to the menu and add a new `case` branch.
   - In `build_agent`: same — add or update `{CLI_AGENT}`'s `docker build` line.
   - **Leave all other agent entries completely unchanged.**

#### If `agent.sh` does not exist:
- Create it from scratch using the target structure above.
- Add `{CLI_AGENT}` as entry 1 in both `run_agent` and `build_agent`.

#### Per-agent `run` command (derive from Reference Dockerfile/README):
- Always include: `sudo docker run --rm -it -v "$(pwd):/app"`
- Host config mount: `-v "$HOME/.{CLI_AGENT_CONFIG_DIR}:<CONTAINER_CONFIG_PATH>"`
  - `{CLI_AGENT_CONFIG_DIR}` is the **short host-side directory name** (e.g., `claude`), used as `$HOME/.{CLI_AGENT_CONFIG_DIR}`.
  - **`<CONTAINER_CONFIG_PATH>`** is the full path inside the container (e.g., `/home/node/.claude`) — extract it from the Reference Dockerfile by looking at `VOLUME`, `COPY --chown`, or `USER`/`WORKDIR` directives.
- Additional config mounts if needed (e.g., individual files like `.claude.json`)
- Required environment variables: `-e VAR_NAME` for any API keys noted in Reference README
- Default agent flags: flags required for non-interactive/autonomous use (e.g., `--dangerously-skip-permissions`, `-a never`, `--yolo`)

**Output:**
- Save as `agent.sh` in the current project directory
- Make executable: `chmod +x agent.sh`
- Preserve all existing agent entries; only add or update `{CLI_AGENT}`

---

### Step 6: Validate the Dockerfile

Run this checklist:
1. Build test succeeds
2. Layer ordering correct
3. Non-root user (UID 1000)
4. Dependencies installed (COPY + RUN)
5. CLI agent works in container
6. Runtimes accessible

---

### CLI Agent Configuration

Document required environment variables (set at runtime, not in Dockerfile).

---

## Important Reminders

- **Strategy A first**: Always check for a project Dockerfile before falling back to Strategy B
- **Pre-install dependencies**: Image should contain all project-level dependencies (via `COPY` + `RUN install`)
- **Deterministic installs**: Prefer verified binaries with checksums over `curl | bash`
- **Lean but ready**: Keep image lean, but prioritize readiness over size
- **Set entrypoint**: Container always starts in agent mode
- **Single unified script**: `agent.sh` is the project's sole agent runner — do not generate per-agent shell scripts
- **Non-destructive updates**: When updating `agent.sh`, only touch the `{CLI_AGENT}` entry — all other agents stay unchanged
"""

def main():
    # Load agent.sh from the same directory as this script (used as a reference example in the prompt).
    script_dir = os.path.dirname(os.path.abspath(__file__))
    run_agent_sh_path = os.path.join(script_dir, "agent.sh")
    if os.path.exists(run_agent_sh_path):
        with open(run_agent_sh_path, "r") as f:
            run_agent_script_content = f.read()
        # Warn if the file exists but doesn't look like a valid agent runner script.
        has_case = 'case "$choice" in' in run_agent_script_content or "case '$choice' in" in run_agent_script_content
        has_run_fn = "run_agent()" in run_agent_script_content or "run_agent ()" in run_agent_script_content
        if not has_case and not has_run_fn:
            print(
                "Warning: agent.sh exists but does not contain the expected structure "
                "('case \"$choice\" in' or 'run_agent()'). "
                "The AI will attempt to parse and update it, but results may vary."
            )
    else:
        run_agent_script_content = "# agent.sh not found — create from scratch using the target structure described in Step 5."

    agents_dir = "agents"
    if not os.path.isdir(agents_dir):
        # Fallback to current directory if agents_dir doesn't exist (depending on where script is run)
        if os.path.isdir("../agents"):
            agents_dir = "../agents"
        else:
            print(f"Error: 'agents' directory not found.")
            sys.exit(1)

    agents = sorted([d for d in os.listdir(agents_dir) if os.path.isdir(os.path.join(agents_dir, d))])
    
    if not agents:
        print(f"Error: No agents found in '{agents_dir}'.")
        sys.exit(1)

    unsupported_agents = [agent for agent in agents if agent not in AGENT_METADATA]
    if unsupported_agents:
        print("Error: Missing metadata for agent(s): " + ", ".join(sorted(unsupported_agents)))
        print("Please add entrypoint/config_dir metadata in AGENT_METADATA.")
        sys.exit(1)

    print("Available agents:")
    for i, agent in enumerate(agents):
        print(f"{i}: {agent}")

    try:
        choice_str = input(f"Choose an agent (0-{len(agents)-1}): ")
        choice = int(choice_str)
        if choice < 0 or choice >= len(agents):
            raise ValueError
    except (ValueError, EOFError):
        print("\nInvalid choice.")
        sys.exit(1)

    selected_agent = agents[choice]
    agent_path = os.path.join(agents_dir, selected_agent)
    
    dockerfile_path = os.path.join(agent_path, "Dockerfile")
    readme_path = os.path.join(agent_path, "README.md")

    dockerfile_content = "Dockerfile not found."
    if os.path.exists(dockerfile_path):
        with open(dockerfile_path, "r") as f:
            dockerfile_content = f.read()

    readme_content = "README.md not found."
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            readme_content = f.read()

    agent_metadata = AGENT_METADATA[selected_agent]
    agent_entrypoint = agent_metadata["entrypoint"]
    agent_config_dir = agent_metadata["config_dir"]

    final_prompt = PROMPT_TEMPLATE.format(
        CLI_AGENT=selected_agent,
        DOCKERFILE_CONTENT=dockerfile_content,
        README_CONTENT=readme_content,
        CLI_AGENT_NAME_LOWER=agent_entrypoint,
        CLI_AGENT_CONFIG_DIR=agent_config_dir,
        RUN_AGENT_SCRIPT_CONTENT=run_agent_script_content,
    )

    print("\n--- GENERATED PROMPT ---\n")
    print(final_prompt)
    print("\n--- END OF PROMPT ---")

if __name__ == "__main__":
    main()
