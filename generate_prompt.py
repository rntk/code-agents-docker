#!/usr/bin/env python3
import os
import sys

# The base prompt template from skills/generate-project-dockerfile/prompt.md
# Updated to refer to embedded content and improved for use with agents.
PROMPT_TEMPLATE = """# Skill: Generate Project-Specific Dockerfile

You are a DevOps engineer specializing in containerized development environments for AI coding agents.

## Objective

Generate a project-specific Dockerfile that gives an AI coding CLI agent everything it needs to work on a given software project.

**Strategy:**
1. **If the project has its own Dockerfile** — extend it by adding the coding agent (Strategy A - preferred)
2. **If the project has no Dockerfile** — choose an appropriate base image, install runtimes and tools, then add the coding agent (Strategy B)

**The generated Dockerfile must pre-install all project dependencies** so the environment is ready for testing and execution immediately.

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

### Step 5: Validate the Dockerfile

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
"""

def main():
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

    # Extract a simple command name for the entrypoint placeholder
    # e.g., 'claude-code' -> 'claude', 'gemini-cli' -> 'gemini'
    agent_name_lower = selected_agent.split('-')[0]

    final_prompt = PROMPT_TEMPLATE.format(
        CLI_AGENT=selected_agent,
        DOCKERFILE_CONTENT=dockerfile_content,
        README_CONTENT=readme_content,
        CLI_AGENT_NAME_LOWER=agent_name_lower
    )

    print("\n--- GENERATED PROMPT ---\n")
    print(final_prompt)
    print("\n--- END OF PROMPT ---")

if __name__ == "__main__":
    main()
