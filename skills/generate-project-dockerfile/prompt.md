# Skill: Generate Project-Specific Dockerfile

You are a DevOps engineer specializing in containerized development environments for AI coding agents.

## Objective

Generate a project-specific Dockerfile that gives an AI coding CLI agent everything it needs to work on a given software project. The strategy is:

1. **If the project has its own Dockerfile** — use it as the starting point and add the coding agent into it (Strategy A)
2. **If the project has no Dockerfile** — use `ubuntu:24.04` as a universal base, install all required runtimes and tools natively, then add the coding agent (Strategy B)

Never copy runtimes between slim Docker images via multi-stage builds — it is fragile. Either reuse the project's proven Dockerfile or start from a full-featured base.

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

| Indicator File/Pattern | Language |
|------------------------|----------|
| `*.py`, `pyproject.toml`, `setup.py`, `setup.cfg`, `Pipfile` | Python |
| `*.js`, `*.mjs`, `*.cjs`, `package.json` | JavaScript (Node.js) |
| `*.ts`, `*.tsx`, `tsconfig.json` | TypeScript |
| `*.go`, `go.mod`, `go.sum` | Go |
| `*.rs`, `Cargo.toml` | Rust |
| `*.java`, `pom.xml`, `build.gradle`, `*.gradle.kts` | Java |
| `*.kt`, `*.kts` | Kotlin |
| `*.rb`, `Gemfile` | Ruby |
| `*.php`, `composer.json` | PHP |
| `*.cs`, `*.csproj`, `*.sln` | C# / .NET |
| `*.c`, `*.h`, `Makefile`, `CMakeLists.txt` | C |
| `*.cpp`, `*.cc`, `*.cxx`, `*.hpp` | C++ |
| `*.swift`, `Package.swift` | Swift |
| `*.ex`, `*.exs`, `mix.exs` | Elixir |
| `*.scala`, `build.sbt` | Scala |
| `*.lua` | Lua |
| `*.zig`, `build.zig` | Zig |
| `*.dart`, `pubspec.yaml` | Dart |
| `*.r`, `*.R`, `DESCRIPTION` | R |
| `*.jl`, `Project.toml` | Julia |
| `*.sh`, `*.bash` | Shell/Bash |

#### 2.2 Package Managers & Dependency Files

| File | Tool | Action |
|------|------|--------|
| `package.json` | npm/yarn/pnpm | Install Node.js if not in base image |
| `package-lock.json` | npm | Use npm for installs |
| `yarn.lock` | yarn | Install yarn |
| `pnpm-lock.yaml` | pnpm | Install pnpm |
| `bun.lockb`, `bun.lock` | bun | Install bun runtime |
| `requirements.txt` | pip | Install Python + pip |
| `pyproject.toml` | pip/poetry/uv | Install Python; check `[build-system]` for tool |
| `Pipfile` | pipenv | Install Python + pipenv |
| `poetry.lock` | poetry | Install Python + poetry |
| `uv.lock` | uv | Install Python + uv |
| `go.mod` | go modules | Install Go |
| `Cargo.toml` | cargo | Install Rust toolchain |
| `Gemfile` | bundler | Install Ruby + bundler |
| `composer.json` | composer | Install PHP + composer |
| `pom.xml` | maven | Install Java + Maven |
| `build.gradle`, `build.gradle.kts` | gradle | Install Java + Gradle |
| `mix.exs` | mix | Install Elixir |
| `pubspec.yaml` | dart/flutter pub | Install Dart/Flutter |

#### 2.3 Testing Frameworks

Look inside config files and dependency lists to detect testing tools:

| Indicator | Framework | Requires |
|-----------|-----------|----------|
| `pytest` in dependencies or `pytest.ini`, `conftest.py`, `pyproject.toml [tool.pytest]` | pytest | Python |
| `unittest` imports in `*.py` | unittest | Python |
| `jest` in `package.json` devDependencies, `jest.config.*` | Jest | Node.js |
| `mocha` in `package.json`, `.mocharc.*` | Mocha | Node.js |
| `vitest` in `package.json`, `vitest.config.*` | Vitest | Node.js |
| `playwright` in dependencies, `playwright.config.*` | Playwright | Node.js + browsers |
| `cypress` in dependencies, `cypress.config.*` | Cypress | Node.js + browsers |
| `go test` patterns, `*_test.go` files | go test | Go |
| `#[cfg(test)]` in `*.rs`, `tests/` dir with Cargo.toml | cargo test | Rust |
| `rspec` in Gemfile, `.rspec`, `spec/` dir | RSpec | Ruby |
| `phpunit` in composer.json, `phpunit.xml` | PHPUnit | PHP |
| `JUnit`, `TestNG` in pom.xml/build.gradle | JUnit/TestNG | Java |

#### 2.4 Build Tools & Task Runners

| File | Tool |
|------|------|
| `Makefile` | make |
| `CMakeLists.txt` | cmake |
| `Taskfile.yml` | task (go-task) |
| `justfile` | just |
| `Rakefile` | rake (Ruby) |
| `Gruntfile.js` | grunt |
| `gulpfile.js` | gulp |
| `turbo.json` | turborepo |
| `nx.json` | nx |
| `webpack.config.*` | webpack |
| `vite.config.*` | vite |
| `rollup.config.*` | rollup |
| `esbuild` in package.json | esbuild |
| `tsup` in package.json | tsup |

#### 2.5 Linters, Formatters & Code Quality

| File | Tool |
|------|------|
| `.eslintrc*`, `eslint.config.*` | ESLint |
| `.prettierrc*`, `prettier.config.*` | Prettier |
| `ruff.toml`, `[tool.ruff]` in pyproject.toml | Ruff |
| `.flake8`, `[flake8]` in setup.cfg | Flake8 |
| `mypy.ini`, `[tool.mypy]` in pyproject.toml | mypy |
| `.rubocop.yml` | RuboCop |
| `clippy` in Cargo.toml | Clippy |
| `golangci-lint` config, `.golangci.yml` | golangci-lint |
| `biome.json` | Biome |

#### 2.6 Database & Infrastructure

| File/Pattern | Service |
|--------------|---------|
| Database URLs, `sqlalchemy`, `diesel`, `prisma`, `drizzle`, `knex`, `typeorm`, `sequelize` in dependencies | Database client libs |
| `docker-compose.yml` referencing services | External service dependencies |
| `.env.example` listing required env vars | Environment configuration hints |
| `redis` in dependencies | Redis client |
| `Procfile` | Process management (Heroku-style) |
| `serverless.yml`, `sam.template.yaml` | Serverless frameworks |

#### 2.7 System-Level Tool Requirements

| Indicator | System Package |
|-----------|---------------|
| `git` usage, `.gitmodules` | git |
| `curl`/`wget` in scripts | curl / wget |
| `ssh` keys or remote access | openssh-client |
| Image processing libraries (`Pillow`, `sharp`) | libjpeg, libpng, etc. |
| `bcrypt`, `argon2` in dependencies | build-essential / gcc |
| `lxml` in Python deps | libxml2-dev, libxslt-dev |
| `psycopg2` (non-binary) in Python deps | libpq-dev |
| `mysqlclient` in Python deps | default-libmysqlclient-dev |
| FFmpeg usage | ffmpeg |
| `cairo`, `pango` in deps | libcairo2-dev, libpango1.0-dev |
| Native Node addons (`node-gyp`) | python3, make, g++ |
| `protobuf` usage | protobuf-compiler |

---

### Step 3: Choose the Base Image Strategy

Before generating anything, decide which strategy to use. Evaluate them **in order** — use the first one that applies.

#### Strategy A: Project Has Its Own Dockerfile (Preferred)

**When to use**: The target project at `{PROJECT_DIR}` contains a `Dockerfile` (or `Dockerfile.dev`, `docker-compose.yml` with a build context, etc.).

**Why**: The project's Dockerfile already solves the hardest problem — it has the correct runtime, system libraries, and build dependencies. You just need to add the AI coding agent on top.

**How**:
1. Read the project's Dockerfile and understand its base image, installed packages, and user setup
2. Extend it by adding the CLI agent installation
3. If the project Dockerfile uses a final `CMD` or `ENTRYPOINT` for the application itself, **replace it** with the CLI agent entrypoint

**Key considerations**:
- If the project uses a multi-stage build, base your work on the **final stage** (the runtime image), not a build stage
- If the project Dockerfile doesn't set up a non-root user, add one
- The project Dockerfile may already `COPY` source code — **remove those lines** since the code will be volume-mounted at runtime
- Remove any `EXPOSE` directives (not needed for a CLI agent)
- Keep all `RUN` lines that install system packages, runtimes, and tools

#### Strategy B: No Project Dockerfile — Use `ubuntu:24.04` (Universal Fallback)

**When to use**: The target project has no Dockerfile, or its Dockerfile is unsuitable (e.g., scratch image, distroless, heavily application-specific).

**Why**: `ubuntu:24.04` provides a full, stable base with `apt-get` access to virtually every package. No brittle multi-stage runtime copying needed — just install what you need natively. This is more reliable than trying to graft runtimes between slim images.

**How**:
1. Start from `ubuntu:24.04`
2. Install all required language runtimes via `apt-get` or official install scripts
3. Install the AI coding CLI agent
4. Install global development tools
5. Set up a non-root user

**Runtime installation methods on Ubuntu:**

| Runtime | Installation |
|---------|-------------|
| **Node.js** | `curl -fsSL https://deb.nodesource.com/setup_24.x \| bash - && apt-get install -y nodejs` |
| **Python** | `apt-get install -y python3 python3-pip python3-venv` (system Python) or install via `deadsnakes` PPA for a specific version |
| **Go** | `curl -fsSL https://go.dev/dl/go1.23.linux-amd64.tar.gz \| tar -C /usr/local -xzf -` + add to PATH |
| **Rust** | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh -s -- -y` (as non-root user) |
| **Ruby** | `apt-get install -y ruby-full` |
| **Java** | `apt-get install -y openjdk-21-jdk` |
| **PHP** | `apt-get install -y php-cli php-mbstring php-xml php-curl` |
| **.NET** | Use Microsoft's install script: `curl -fsSL https://dot.net/v1/dotnet-install.sh \| bash -s -- --channel 8.0` |
| **Elixir** | `apt-get install -y elixir` |

**CLI agent installation on Ubuntu:**

| CLI Agent | Installation |
|-----------|-------------|
| `claude-code` | Requires Node.js. `npm install -g @anthropic-ai/claude-code` |
| `codex-cli` | Requires Node.js. `npm install -g @openai/codex` |
| `copilot-cli` | Requires Node.js. `npm install -g @github/copilot` |
| `gemini-cli` | Requires Node.js. `npm install -g @google/gemini-cli` |
| `devstral-cli` | Requires Python + uv. `pip install uv && uv tool install mistral-vibe` |
| `kimi-cli` | Requires Python. `curl -L code.kimi.com/install.sh \| bash` |

---

### Step 4: Generate the Project-Specific Dockerfile

Using the information from Steps 1–3, create a Dockerfile. Follow these rules strictly:

#### 4.1 Architecture Rules

1. **Install system packages early** (before switching to non-root user). Group all `apt-get install` commands into a single `RUN` layer. Always clean up: `&& rm -rf /var/lib/apt/lists/*`

2. **Install language runtimes before the CLI tool**. The AI agent CLI must be installed after all runtimes are available so it can detect and use them.

3. **Do NOT install project dependencies** (no `npm install`, `pip install -r requirements.txt`, etc. for the project itself). The Dockerfile sets up the environment — the AI agent will handle project dependency installation at runtime.

4. **DO install global tools** that the agent needs for analysis, testing, and development:
   - Testing runners (pytest, jest globally if needed)
   - Linters/formatters the project uses
   - Build tools (make, cmake, etc.)
   - Package managers (yarn, pnpm, poetry, etc.)

5. **Set the ENTRYPOINT/CMD** to the CLI agent command (e.g., `claude`, `codex`, `gemini`).

6. **Always create a non-root user** if one doesn't exist. Use `appuser` with UID 1000.

7. **Do NOT COPY project source code**. The project directory is volume-mounted at `/app` at runtime.

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
#  EXPOSE directives, and the application CMD/ENTRYPOINT.)

FROM {PROJECT_BASE_IMAGE}

# ... (system packages and runtime setup from project Dockerfile) ...

# --- Install the AI coding CLI ---
# For Node.js-based agents (install Node.js first if not already present):
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
RUN chown -R appuser:appuser /app
RUN mkdir -p /home/appuser/.{cli_config_dir} && \
    chown -R appuser:appuser /home/appuser/.{cli_config_dir}
USER appuser

ENV PATH="/home/appuser/.local/bin:$PATH"

# --- CLI agent entrypoint (replaces the project's application CMD) ---
ENTRYPOINT ["{CLI_COMMAND}"]
```

#### 4.3 Template for Strategy B (Ubuntu Universal Base)

```dockerfile
# =============================================================================
# Project-Specific Dockerfile for {CLI_AGENT}
# Generated for: {PROJECT_NAME}
# Base: ubuntu:24.04 (universal)
# Detected stack: {SUMMARY_OF_DETECTED_TECH}
# =============================================================================

FROM ubuntu:24.04

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
# RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
#     apt-get install -y nodejs

# Example for Python:
# RUN apt-get update && apt-get install -y python3 python3-pip python3-venv && \
#     rm -rf /var/lib/apt/lists/*

# --- Install the AI coding CLI ---
ARG {CLI}_VERSION=latest
# (use the appropriate install method from the reference Dockerfile)
# RUN npm install -g "{CLI_NPM_PACKAGE}@${{{CLI}_VERSION}}"

# --- Install global development tools ---
# RUN pip install pytest ruff mypy
# RUN npm install -g jest eslint prettier

# --- Non-root user setup ---
RUN useradd -r -m -u 1000 -s /bin/bash appuser

WORKDIR /app
RUN chown -R appuser:appuser /app
RUN mkdir -p /home/appuser/.{cli_config_dir} && \
    chown -R appuser:appuser /home/appuser/.{cli_config_dir}

USER appuser
ENV PATH="/home/appuser/.local/bin:$PATH"

ENTRYPOINT ["{CLI_COMMAND}"]
```

#### 4.4 Naming & Output

- Save the generated Dockerfile as `Dockerfile.{project_name}` in the `{CLI_AGENT}/` directory
- Also generate a companion `README.{project_name}.md` with:
  - Which strategy was used (A or B) and why
  - Detected technology stack summary
  - Build command
  - Run command with all necessary volume mounts and env vars
  - List of pre-installed tools and why each was included

---

### Step 5: Validate the Dockerfile

After generating the Dockerfile, verify:

1. **Syntax**: The Dockerfile is valid (no obvious syntax errors)
2. **Layer ordering**: System packages -> runtimes -> CLI tool -> global tools -> user switch -> entrypoint
3. **User consistency**: The non-root user is set up and matches throughout the file
4. **No project deps**: Confirm you did NOT add `RUN npm install` or `RUN pip install -r requirements.txt` for the project's own dependencies
5. **No source COPY**: Confirm you did NOT `COPY` project source code into the image
6. **Entrypoint correct**: The CLI agent entrypoint is set (not the project's application entrypoint)
7. **All detected tools accounted for**: Cross-reference Step 2 findings with installed packages
8. **Runtime test**: Mentally verify — "Can the AI agent run `pytest`, `npm test`, `go test`, etc. inside this container?"

---

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
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Claude Code CLI
ARG CLAUDE_VERSION=latest
RUN npm install -g "@anthropic-ai/claude-code@${CLAUDE_VERSION}"

# Global dev tools for the project
RUN pip install pytest ruff mypy

# Non-root user
RUN useradd -r -m -u 1000 -s /bin/bash appuser
WORKDIR /app
RUN chown -R appuser:appuser /app
RUN mkdir -p /home/appuser/.claude && chown -R appuser:appuser /home/appuser/.claude
USER appuser
ENV PATH="/home/appuser/.local/bin:$PATH"

# NOTE: No COPY, no EXPOSE, no application CMD
# Project code is volume-mounted at /app at runtime
ENTRYPOINT ["claude"]
```

**What changed vs the project's original Dockerfile:**
- Removed `COPY . .` and `RUN poetry install` (agent handles deps at runtime)
- Removed `EXPOSE 8000` and `CMD ["python", "manage.py", "runserver"]`
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

# Go runtime
RUN curl -fsSL https://go.dev/dl/go1.23.linux-amd64.tar.gz | tar -C /usr/local -xzf -
ENV PATH="/usr/local/go/bin:$PATH"

# Node.js (required for Claude Code)
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Claude Code CLI
ARG CLAUDE_VERSION=latest
RUN npm install -g "@anthropic-ai/claude-code@${CLAUDE_VERSION}"

# golangci-lint
RUN curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | \
    sh -s -- -b /usr/local/bin

# Non-root user
RUN useradd -r -m -u 1000 -s /bin/bash appuser
WORKDIR /app
RUN chown -R appuser:appuser /app
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
- **Do not copy runtimes between images**: Never use multi-stage builds to copy a runtime (Python, Node, Go) from one slim image into another. Use `ubuntu:24.04` and install natively instead — it is simpler and more reliable.
- The goal is to give the AI coding agent everything it needs to **analyze, test, lint, and build** the target project
- The agent itself will clone/mount the project and install project-level dependencies at runtime
- Keep the image as lean as possible — only install what is actually detected in the project
- When in doubt about a system library, include it — a missing library at runtime is worse than a slightly larger image
- Always test your mental model: "Can the AI agent run the project's test suite with this Dockerfile?" If not, something is missing
