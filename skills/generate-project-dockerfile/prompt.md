# Skill: Generate Project-Specific Dockerfile

You are a DevOps engineer specializing in containerized development environments for AI coding agents.

## Objective

Generate a project-specific Dockerfile that gives an AI coding CLI agent everything it needs to work on a given software project. The strategy is:

1. **If the project has its own Dockerfile** — use it as the starting point and add the coding agent into it (Strategy A)
2. **If the project has no Dockerfile** — choose an appropriate base image, install all required runtimes and tools natively, then add the coding agent (Strategy B)

Prefer reusing the project's proven Dockerfile when available. For projects without Dockerfiles, select a base image that matches the project's needs while keeping images lean, reproducible, and secure.

## Inputs

You will be provided with:

1. **`PROJECT_DIR`** — Absolute path to the target project directory to analyze
2. **`CLI_AGENT`** — Name of the AI coding CLI to use (one of: `claude-code`, `codex-cli`, `copilot-cli`, `devstral-cli`, `gemini-cli`, `kimi-cli`)
3. **`DOCKERFILES_REPO`** — Path to this repository containing the base Dockerfile templates

## Procedure

Follow these steps in order. Do NOT skip steps.

---

### Step 1: Read the Reference Dockerfile

Read the Dockerfile at `{DOCKERFILES_REPO}/{CLI_AGENT}/Dockerfile`. This is the **reference** for how the CLI agent is installed. Extract:

- How the CLI is installed (e.g., `npm install -g @anthropic-ai/claude-code`, `uv tool install mistral-vibe`)
- What runtime it requires (Node.js for most, Python for devstral/kimi)
- The entrypoint command (e.g., `claude`, `codex`, `gemini`, `vibe`, `kimi`)
- Config directories it creates (e.g., `/home/node/.claude`)
- Any build ARGs for version pinning

You will use these facts to add the CLI agent into the generated Dockerfile.

---

### Step 2: Analyze the Target Project

Scan `{PROJECT_DIR}` to detect the project's technology stack. Check for the presence of the following files and directories. For each detected item, record what it implies.

#### 2.1 Programming Languages

Scan for language files and config files:
- **Python**: `*.py`, `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile`
- **JavaScript/Node.js**: `*.js`, `*.mjs`, `package.json`, `yarn.lock`, `pnpm-lock.yaml`
- **TypeScript**: `*.ts`, `*.tsx`, `tsconfig.json`
- **Go**: `*.go`, `go.mod`, `go.sum`
- **Rust**: `*.rs`, `Cargo.toml`
- **Java**: `*.java`, `pom.xml`, `build.gradle`
- **C/C++**: `*.c`, `*.cpp`, `Makefile`, `CMakeLists.txt`
- **And more**: Ruby (`*.rb`, `Gemfile`), PHP (`*.php`, `composer.json`), .NET (`*.cs`, `*.csproj`), etc.

#### 2.2 Package Managers & Build Tools

| File | Tool | Action |
|------|------|--------|
| `package.json` | npm/yarn/pnpm/bun | Install Node.js |
| `requirements.txt`, `pyproject.toml` | pip/poetry/uv | Install Python |
| `go.mod` | go modules | Install Go |
| `Cargo.toml` | cargo | Install Rust |
| `Gemfile` | bundler | Install Ruby |
| `composer.json` | composer | Install PHP |
| `pom.xml` | maven | Install Java + Maven |
| `build.gradle` | gradle | Install Java + Gradle |
| `Makefile` | make | Install make |
| `CMakeLists.txt` | cmake | Install cmake |

#### 2.3 Testing & Code Quality

Look for testing frameworks and quality tools in dependencies/configs:
- **Python**: pytest, unittest, ruff, mypy, flake8
- **Node.js**: jest, mocha, vitest, eslint, prettier
- **Go**: go test, golangci-lint
- **Rust**: cargo test, clippy
- **Java**: JUnit, TestNG
- **And more**: RSpec (Ruby), PHPUnit (PHP), etc.

#### 2.4 System Dependencies

Common system packages needed:
- **Database clients**: libpq-dev (PostgreSQL), default-libmysqlclient-dev (MySQL)
- **Image processing**: libjpeg, libpng, ffmpeg
- **XML/HTML**: libxml2-dev, libxslt-dev
- **Cryptography**: build-essential, gcc
- **Native addons**: python3, make, g++

---

### Step 3: Choose the Base Image Strategy

Before generating anything, decide which strategy to use. Evaluate them **in order** — use the first one that applies.

#### Strategy A: Project Has Its Own Dockerfile (Preferred)

**When to use**: The target project at `{PROJECT_DIR}` contains a `Dockerfile` (or `Dockerfile.dev`, `docker-compose.yml` with a build context, etc.).

**Why**: The project's Dockerfile already solves the hardest problem — it has the correct runtime, system libraries, and build dependencies. You just need to add the AI coding agent on top.

**How**:
1. Read the project's Dockerfile and understand its base image, installed packages, and user setup
2. Extend it by adding the CLI agent installation
3. Set the CLI agent executable as the container `ENTRYPOINT` for agent mode

**Key considerations**:
- If the project uses a multi-stage build, base your work on the **final stage** (the runtime image), not a build stage
- If the project Dockerfile doesn't set up a non-root user, add one
- The project Dockerfile may already `COPY` source code — remove only source-copy lines; keep `COPY` of required runtime assets (certs, scripts, migrations, config templates)
- Remove `EXPOSE` directives unless they are still needed by retained startup or helper tooling
- Keep all `RUN` lines that install system packages, runtimes, and tools
- Keep existing init/wrapper scripts unless they are clearly app-server-only and conflict with agent mode

#### Strategy B: No Project Dockerfile — Choose Appropriate Base

**When to use**: The target project has no Dockerfile, or its Dockerfile is unsuitable (e.g., scratch image, distroless, heavily application-specific).

**Base image decision tree**:
1. **Official slim image available for primary runtime?** → Prefer Debian/Ubuntu slim images first (e.g., `node:20-slim`, `python:3.13-slim`)
2. **Multiple heavy runtimes or complex system deps?** → Use `ubuntu:24.04` for broad compatibility
3. **Alpine considered?** → Use Alpine only when dependencies are known to be musl-compatible and native extensions are minimal

**Why**: Debian/Ubuntu slim images provide strong compatibility with modest size. Ubuntu provides the broadest compatibility but at higher image size. Alpine is smaller but can break native dependencies (musl vs glibc).

**How**:
1. Start from the chosen base image
2. Install all required language runtimes via distro packages or verified official binaries
3. Install the AI coding CLI agent
4. Install only explicitly detected global development tools that are not already project-managed
5. Set up a non-root user

**Runtime installation methods on Ubuntu:**

| Runtime | Installation |
|---------|-------------|
| **Node.js** | Prefer distro package or official Node image. If using NodeSource, add signed repo key + apt source (avoid `curl \| bash`) |
| **Python** | `apt-get install -y python3 python3-pip python3-venv` (system Python) or install via `deadsnakes` PPA for a specific version |
| **Go** | Download official tarball per arch (`TARGETARCH`) and verify checksum before extract |
| **Rust** | Install rustup via verified installer/checksum, as non-root user |
| **Ruby** | `apt-get install -y ruby-full` |
| **Java** | `apt-get install -y openjdk-21-jdk` |
| **PHP** | `apt-get install -y php-cli php-mbstring php-xml php-curl` |
| **.NET** | Prefer Microsoft apt repo packages for reproducible installs |
| **Elixir** | `apt-get install -y elixir` |

**CLI agent installation on Ubuntu:**

| CLI Agent | Installation |
|-----------|-------------|
| `claude-code` | Requires Node.js. `npm install -g @anthropic-ai/claude-code` |
| `codex-cli` | Requires Node.js. `npm install -g @openai/codex` |
| `copilot-cli` | Requires Node.js. `npm install -g @github/copilot` |
| `gemini-cli` | Requires Node.js. `npm install -g @google/gemini-cli` |
| `devstral-cli` | Requires Python + uv. `pip install uv && uv tool install mistral-vibe` |
| `kimi-cli` | Requires Python. Prefer a versioned package/binary install from the reference Dockerfile; avoid unverified shell piping |

---

### Step 3.5: Consider Architecture & Platform

**Multi-platform builds**: Support both AMD64 and ARM64 architectures when possible. Use `docker buildx build --platform linux/amd64,linux/arm64` for builds. Note that some runtime installers (like Go downloads) may need platform-specific URLs.

**Performance considerations**: On ARM64 systems (M1/M2 Macs), prefer native ARM64 images over Rosetta translation. Official slim images often have better ARM64 support than Ubuntu.

When downloading runtime tarballs, map architecture explicitly:

```dockerfile
ARG TARGETARCH
RUN case "$TARGETARCH" in \
      amd64) GO_ARCH='amd64' ;; \
      arm64) GO_ARCH='arm64' ;; \
      *) echo "Unsupported arch: $TARGETARCH" && exit 1 ;; \
    esac && \
    curl -fsSLO "https://go.dev/dl/go${GO_VERSION}.linux-${GO_ARCH}.tar.gz" && \
    curl -fsSLO "https://go.dev/dl/go${GO_VERSION}.linux-${GO_ARCH}.tar.gz.sha256" && \
    sha256sum -c "go${GO_VERSION}.linux-${GO_ARCH}.tar.gz.sha256" && \
    tar -C /usr/local -xzf "go${GO_VERSION}.linux-${GO_ARCH}.tar.gz"
```

---

### Step 4: Generate the Project-Specific Dockerfile

Using the information from Steps 1–3, create a Dockerfile. Follow these rules strictly:

#### 4.1 Architecture Rules

1. **Install system packages early** (before switching to non-root user). Group all `apt-get install` commands into a single `RUN` layer. Always clean up: `&& rm -rf /var/lib/apt/lists/*`

2. **Install language runtimes before the CLI tool**. The AI agent CLI must be installed after all runtimes are available so it can detect and use them.

3. **Do NOT install project dependencies** (no `npm install`, `pip install -r requirements.txt`, etc. for the project itself). The Dockerfile sets up the environment — the AI agent will handle project dependency installation at runtime.

4. **Install global tools sparingly**:
   - Install a global tool only if explicitly detected in project config and not already project-managed
   - Prefer runtime-native execution first (e.g., `npm test`, `npx eslint`, `python -m pytest`) before adding global installs
   - Keep global installs version-pinned (`tool@x.y.z`) when possible
   - **Do NOT install**: Project dependencies from `requirements.txt`, `package.json` dependencies, or `go.mod` — let the agent handle these at runtime

5. **Set `ENTRYPOINT`** to the CLI agent command (e.g., `ENTRYPOINT ["claude"]`).

6. **Always create a non-root user** if one doesn't exist. Use `appuser` with UID 1000.

7. **Do NOT COPY project source code**. The project directory is volume-mounted at `/app` at runtime.

8. **Layer ordering for cache efficiency**: Order layers from least to most frequently changing:
   - System packages (rarely change)
   - Language runtimes (change with version updates)
   - CLI agent (changes with updates)
   - Global tools (may change with project needs)
   - User setup and entrypoint (rarely change)

#### 4.2 Template for Strategy A (Project Dockerfile as Base)

```dockerfile
# =============================================================================
# Project-Specific Dockerfile for {CLI_AGENT}
# Generated for: {PROJECT_NAME}
# Based on: project's own Dockerfile
# Detected stack: {SUMMARY_OF_DETECTED_TECH}
# =============================================================================

# --- Reproduce the project's runtime environment ---
# (Adapted from the project's Dockerfile — keep all RUN lines that install
#  system packages, runtimes, and tools. Remove COPY lines for source code,
#  optional EXPOSE directives, and app-server-only command defaults.)

FROM {PROJECT_BASE_IMAGE}

# ... (system packages and runtime setup from project Dockerfile) ...

# --- Install the AI coding CLI ---
# CLI versioning: default to latest; allow override via --build-arg for reproducibility
ARG {CLI}_VERSION=latest
RUN npm install -g "{CLI_NPM_PACKAGE}@${{{CLI}_VERSION}}"

# --- Install global development tools detected in the project ---
# RUN pip install pytest ruff mypy
# RUN npm install -g jest eslint prettier

# --- Working directory ---
WORKDIR /app

# --- Non-root user setup ---
# (reuse the project's user if one exists, otherwise create one)
RUN useradd -r -m -u 1000 appuser || true
RUN mkdir -p /app && chown appuser:appuser /app
RUN mkdir -p /home/appuser/.{cli_config_dir} && \
    chown -R appuser:appuser /home/appuser/.{cli_config_dir}
USER appuser

ENV PATH="/home/appuser/.local/bin:$PATH"

# --- CLI agent entrypoint (agent mode default) ---
ENTRYPOINT ["{CLI_COMMAND}"]
```

#### 4.3 Template for Strategy B (Slim/Ubuntu Base)

```dockerfile
# =============================================================================
# Project-Specific Dockerfile for {CLI_AGENT}
# Generated for: {PROJECT_NAME}
# Base: {CHOSEN_BASE_IMAGE}
# Detected stack: {SUMMARY_OF_DETECTED_TECH}
# =============================================================================

FROM {CHOSEN_BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive

# --- System dependencies (single layer) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    make \
    {DETECTED_SYSTEM_PACKAGES} \
    && rm -rf /var/lib/apt/lists/*

# --- Language runtimes ---
# Install each runtime needed by the project.
# Example for Node.js:
# RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm && \
#     rm -rf /var/lib/apt/lists/*

# Example for Python:
# RUN apt-get update && apt-get install -y python3 python3-pip python3-venv && \
#     rm -rf /var/lib/apt/lists/*

# --- Install the AI coding CLI ---
ARG {CLI}_VERSION=latest
# (use the appropriate install method from the reference Dockerfile)
# RUN npm install -g "{CLI_NPM_PACKAGE}@${{{CLI}_VERSION}}"

# --- Install only required global tools (if detected) ---
# RUN pip install "ruff==0.6.9"
# RUN npm install -g "eslint@9.12.0"

# --- Non-root user setup ---
RUN useradd -r -m -u 1000 -s /bin/bash appuser

WORKDIR /app
RUN mkdir -p /app && chown appuser:appuser /app
RUN mkdir -p /home/appuser/.{cli_config_dir} && \
    chown -R appuser:appuser /home/appuser/.{cli_config_dir}

USER appuser
ENV PATH="/home/appuser/.local/bin:$PATH"

ENTRYPOINT ["{CLI_COMMAND}"]
```

#### 4.4 Naming & Output

- Save the generated Dockerfile as `Dockerfile.{CLI_AGENT}` in the `{CLI_AGENT}/` directory
- Also create/update a single `README.agents_docker.md` with just a couple instructions of how to build and run
- If generating a `.dockerignore`, exclude: `node_modules/`, `venv/`, `__pycache__/`, `.git/`, build artifacts, test outputs, IDE configs

#### 4.5 Output Contract (Must/Must-Not)

- **Must include**: chosen strategy (`A` or `B`), detected stack summary, and explicit reason for base image choice
- **Must include**: CLI version `ARG` defaulting to `latest`, non-root user, `/app` workdir, and cleanup of package manager caches
- **Must not include**: unverified `curl | bash` installers, project dependency install commands, or `COPY . .` for project source
- **Must explain**: any global tool installed and why it was needed

---

### Step 5: Validate and Verify the Dockerfile

After generating the Dockerfile, run this checklist:

1. **Syntax and build**: `docker build -t test-{cli-agent} -f Dockerfile.{cli-agent} .` succeeds
2. **Layer ordering**: System packages -> runtimes -> CLI tool -> optional global tools -> user switch -> entrypoint
3. **User consistency**: The non-root user is set up and matches throughout the file
4. **No project deps**: Confirm you did NOT add `RUN npm install` or `RUN pip install -r requirements.txt` for the project's own dependencies
5. **No source COPY**: Confirm you did NOT copy project source code into the image (except required runtime assets)
6. **Entrypoint rule**: `ENTRYPOINT` is set to the CLI agent command
7. **All detected tools accounted for**: Cross-reference Step 2 findings with installed packages
8. **CLI command works**: `docker run --rm test-{cli-agent} --version`
9. **Verify runtimes are accessible**: 
   - `docker run --rm test-{cli-agent} python --version` (if Python project)
   - `docker run --rm test-{cli-agent} node --version` (if Node.js project)
   - `docker run --rm test-{cli-agent} go version` (if Go project)
10. **Check user permissions**: `docker run --rm test-{cli-agent} whoami` (should be appuser)
11. **Test optional global tools**: `docker run --rm test-{cli-agent} pytest --version` (only if installed)

---

### CLI Agent Configuration

The generated Dockerfile should NOT include API keys, but should document required environment variables for runtime:

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

- **CLI agent**: Default to latest via `ARG ...=latest`; users can pin a specific version with `--build-arg` when reproducibility is needed
- **Language runtimes**: Pin major version, float minor (e.g., `node:20` not `node:latest`)
- **System packages**: Use distro defaults (they're tested together)
- **Global tools**: Pin to specific versions when installed

## Examples

### Example 1: Strategy A — Project Has a Dockerfile

**Input:**
- `PROJECT_DIR`: `/home/user/my-django-app` (Django project with its own Dockerfile)
- `CLI_AGENT`: `claude-code`
- `DOCKERFILES_REPO`: `/home/user/ai-coding-cli-containers`

**Project's existing Dockerfile:**
```dockerfile
FROM python:3.13-slim
RUN apt-get update && apt-get install -y libpq-dev build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install poetry
WORKDIR /app
COPY . .
RUN poetry install
EXPOSE 8000
CMD ["python", "manage.py", "runserver"]
```

**Analysis detects:** Python 3.x, poetry, pytest, ruff, mypy, PostgreSQL (psycopg2), Makefile

**Generated Dockerfile (Strategy A):**
```dockerfile
# Based on project's own Dockerfile — already has Python 3.13, libpq-dev, poetry
FROM python:3.13-slim

# System packages (from project Dockerfile + extras for the agent)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev build-essential make git curl \
    && rm -rf /var/lib/apt/lists/*

# Python package manager (from project)
RUN pip install poetry

# Node.js (required for Claude Code CLI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# Claude Code CLI
ARG CLAUDE_VERSION=latest
RUN npm install -g "@anthropic-ai/claude-code@${CLAUDE_VERSION}"

# Global dev tools for the project
RUN pip install pytest ruff mypy

# Non-root user
RUN useradd -r -m -u 1000 -s /bin/bash appuser
WORKDIR /app
RUN mkdir -p /app && chown appuser:appuser /app
RUN mkdir -p /home/appuser/.claude && chown -R appuser:appuser /home/appuser/.claude
USER appuser
ENV PATH="/home/appuser/.local/bin:$PATH"

# NOTE: No COPY, no EXPOSE, no application CMD
# Project code is volume-mounted at /app at runtime
ENTRYPOINT ["claude"]
```

**What changed vs the project's original Dockerfile:**
- Removed `COPY . .` and `RUN poetry install` (agent handles deps at runtime)
- Replaced app default command with `ENTRYPOINT ["claude"]` for agent mode
- Added Node.js (required by Claude Code)
- Added Claude Code CLI
- Added global dev tools: pytest, ruff, mypy
- Added non-root user setup
- Set `ENTRYPOINT ["claude"]`

---

### Example 2: Strategy B — No Project Dockerfile

**Input:**
- `PROJECT_DIR`: `/home/user/my-go-api` (Go API with no Dockerfile)
- `CLI_AGENT`: `claude-code`
- `DOCKERFILES_REPO`: `/home/user/ai-coding-cli-containers`

**Analysis detects:** Go 1.23, `go.mod`, `*_test.go` files, golangci-lint config, Makefile

**Generated Dockerfile (Strategy B):**
```dockerfile
FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git make \
    && rm -rf /var/lib/apt/lists/*

# Go runtime (multi-arch aware)
ARG GO_VERSION=1.23.7
ARG TARGETARCH
RUN case "$TARGETARCH" in \
      amd64) GO_ARCH='amd64' ;; \
      arm64) GO_ARCH='arm64' ;; \
      *) echo "Unsupported arch: $TARGETARCH" && exit 1 ;; \
    esac && \
    curl -fsSLO "https://go.dev/dl/go${GO_VERSION}.linux-${GO_ARCH}.tar.gz" && \
    curl -fsSLO "https://go.dev/dl/go${GO_VERSION}.linux-${GO_ARCH}.tar.gz.sha256" && \
    sha256sum -c "go${GO_VERSION}.linux-${GO_ARCH}.tar.gz.sha256" && \
    tar -C /usr/local -xzf "go${GO_VERSION}.linux-${GO_ARCH}.tar.gz"
ENV PATH="/usr/local/go/bin:$PATH"

# Node.js (required for Claude Code)
RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# Claude Code CLI
ARG CLAUDE_VERSION=latest
RUN npm install -g "@anthropic-ai/claude-code@${CLAUDE_VERSION}"

# golangci-lint (optional; install only if detected, pinned version preferred)
# RUN curl -fsSLO https://github.com/golangci/golangci-lint/releases/download/v1.61.0/golangci-lint-1.61.0-linux-${GO_ARCH}.tar.gz

# Non-root user
RUN useradd -r -m -u 1000 -s /bin/bash appuser
WORKDIR /app
RUN mkdir -p /app && chown appuser:appuser /app
RUN mkdir -p /home/appuser/.claude && chown -R appuser:appuser /home/appuser/.claude
RUN mkdir -p /home/appuser/go && chown -R appuser:appuser /home/appuser/go
USER appuser
ENV GOPATH="/home/appuser/go"
ENV PATH="/home/appuser/go/bin:$PATH"

ENTRYPOINT ["claude"]
```

---

## Important Reminders

- **Strategy A first**: Always check for a project Dockerfile before falling back to Strategy B. The project's own Dockerfile is the most reliable source of truth for what the project needs.
- **Multi-stage builds**: Safe when using compatible official images. Avoid copying runtimes between incompatible images.
- The goal is to give the AI coding agent everything it needs to **analyze, test, lint, and build** the target project
- The agent itself will clone/mount the project and install project-level dependencies at runtime
- Keep the image as lean as possible — only install what is actually detected in the project
- Prefer deterministic installs over convenience scripts (`curl | bash`)
- Set `ENTRYPOINT` to the agent CLI so the container always starts in agent mode
