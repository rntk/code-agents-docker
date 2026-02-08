# Skill: Generate Project-Specific Dockerfile

You are a DevOps engineer specializing in containerized development environments for AI coding agents.

## Objective

Generate a project-specific Dockerfile that gives an AI coding CLI agent everything it needs to work on a given software project.

**Strategy:**
1. **If the project has its own Dockerfile** — extend it by adding the coding agent (Strategy A - preferred)
2. **If the project has no Dockerfile** — choose an appropriate base image, install runtimes and tools, then add the coding agent (Strategy B)

**The generated Dockerfile must pre-install all project dependencies** so the environment is ready for testing and execution immediately.

## Inputs

Name of the AI coding CLI (`claude-code`, `codex-cli`, `copilot-cli`, `devstral-cli`, `gemini-cli`, `kimi-cli`)

---

### Step 1: Read the Reference Dockerfile

Read `{DOCKERFILES_REPO}/{CLI_AGENT}/Dockerfile` to extract:
- CLI installation method (e.g., `npm install -g @anthropic-ai/claude-code`)
- Required runtime (Node.js for most, Python for devstral/kimi)
- Entrypoint command (e.g., `claude`, `codex`, `gemini`)
- Config directories (e.g., `/home/node/.claude`)
- Build ARGs for version pinning

Also read `{DOCKERFILES_REPO}/{CLI_AGENT}/README.md` to extract:
- Run examples and required parameters (e.g., mounting config directories, environment variables, command-line flags like `-a never` for codex-cli)
- Any agent-specific runtime instructions or configurations

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
RUN case "$TARGETARCH" in \
      amd64) ARCH='amd64' ;; \
      arm64) ARCH='arm64' ;; \
      *) echo "Unsupported: $TARGETARCH" && exit 1 ;; \
    esac && \
    curl -fsSLO "https://example.com/tool-${ARCH}.tar.gz" && \
    curl -fsSLO "https://example.com/tool-${ARCH}.tar.gz.sha256" && \
    sha256sum -c "tool-${ARCH}.tar.gz.sha256"
```

---

### Step 4: Generate the Dockerfile

**Reference Examples:**

Before generating, examine existing project-specific Dockerfiles in `{DOCKERFILES_REPO}/` for similar technology stacks. Look for patterns in:
- How system dependencies are installed
- How project dependencies are handled
- How runtimes are installed for multi-language projects
- How the CLI agent is integrated

**Core Requirements:**

1. **Layer ordering** (least to most frequently changing): System packages → Language runtimes → Project dependencies → CLI agent → Global tools → User setup → Entrypoint

2. **System packages**: Install early, group `apt-get` commands, clean up: `&& rm -rf /var/lib/apt/lists/*`

3. **Project dependencies**: MUST `COPY` manifest files + `RUN` install commands (e.g., `COPY package.json ./ && RUN npm install`)

4. **Global tools**: Install sparingly, only if not project-managed. Version-pin when possible.

5. **Non-root user**: Always create `appuser` (UID 1000) if missing

6. **Entrypoint**: Set to CLI agent command (e.g., `ENTRYPOINT ["claude"]`)

7. **Source code**: Optional `COPY . .` after dependency install. Agent typically volume-mounts at runtime.

8. **Header comment**: Include generated-for project name, strategy used, base image, and detected tech stack

**Output:**
- Save as `Dockerfile.{CLI_AGENT}` in the current project directory
- Add brief build/run instructions as comments at the top of the Dockerfile (keep it concise, not wordy). Include the generated-for project name, strategy used, base image, detected tech stack, required environment variables, and complete run examples from the agent-specific README (e.g., mounting config directories, command-line parameters like `-a never` for codex-cli).

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

1. **Build test**: `docker build -t test-{cli-agent} -f Dockerfile.{cli-agent} .` succeeds
2. **Layer ordering**: Verify correct sequence (system → runtimes → deps → CLI → user → entrypoint)
3. **Non-root user**: Consistent throughout, UID 1000
4. **Dependencies installed**: Confirm `COPY` + `RUN` for project dependencies
5. **CLI works**: `docker run --rm test-{cli-agent} --version`
6. **Runtimes accessible**: Test runtime commands (e.g., `python --version`, `node --version`)
7. **User check**: `docker run --rm test-{cli-agent} whoami` → should be `appuser`

---

### CLI Agent Configuration

Document required environment variables (set at runtime, not in Dockerfile):

```dockerfile
# Example environment variables (set at runtime):
# - ANTHROPIC_API_KEY (for claude-code)
# - OPENAI_API_KEY (for codex-cli)
# - GITHUB_TOKEN (for copilot-cli)
# - GOOGLE_API_KEY (for gemini-cli)
# Run with: docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY ...
```

---

### Version Pinning Strategy

- **CLI agent**: Default to latest via `ARG ...=latest`; users can pin with `--build-arg`
- **Language runtimes**: Pin major version, float minor (e.g., `node:20`)
- **System packages**: Use distro defaults
- **Global tools**: Pin to specific versions when installed

---

## Important Reminders

- **Strategy A first**: Always check for a project Dockerfile before falling back to Strategy B
- **Pre-install dependencies**: Image should contain all project-level dependencies (via `COPY` + `RUN install`)
- **Deterministic installs**: Prefer verified binaries with checksums over `curl | bash`
- **Lean but ready**: Keep image lean, but prioritize readiness over size
- **Set entrypoint**: Container always starts in agent mode
