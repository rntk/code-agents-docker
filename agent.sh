#!/bin/bash

execute() {
    echo -e "\033[1;34m[EXECUTING]\033[0m: $*"
    "$@"
}

run_agent() {
    echo "Available AI Agents:"
    echo "1. claude-code"
    echo "2. codex-cli"
    echo "3. copilot-cli"
    echo "4. codespeak"
    echo "5. devstral-cli"
    echo "6. gemini-cli"
    echo "7. junie-cli"
    echo "8. kimi-cli"
    echo "9. kiro-cli"
    echo "10. qwen-code"

    read -rp "Select agent (1-10): " choice

    case "$choice" in
        1) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.claude:/home/node/.claude" -v "$HOME/.claude/.claude.json:/home/node/.claude.json" -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY claude-code:latest --verbose --dangerously-skip-permissions ;;
        2) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.codex:/home/node/.codex" -e OPENAI_API_KEY=$OPENAI_API_KEY codex-cli:latest -a never --sandbox danger-full-access ;;
        3) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.copilot:/home/node/.copilot" -e GITHUB_API_KEY=$GITHUB_API_KEY copilot-cli:latest --allow-all ;;
        4) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.codespeak:/home/codespeak/.codespeak" -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY --entrypoint /bin/bash codespeak:latest ;;
        5) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.vibe:/home/appuser/.vibe" -e MISTRAL_API_KEY=$MISTRAL_API_KEY devstral-cli:latest ;;
        6) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.gemini:/home/node/.gemini" -e GEMINI_API_KEY=$GEMINI_API_KEY gemini-cli:latest --approval-mode=yolo ;;
        7) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.junie:/home/ubuntu/.junie" -e JUNIE_API_KEY=$JUNIE_API_KEY junie-cli:latest --brave ;;
        8) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.kimi:/home/appuser/.kimi" kimi-cli:latest ;;
        9) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.kiro:/home/ubuntu/.kiro" -v "$HOME/.local/share/kiro-cli:/home/ubuntu/.local/share/kiro-cli" kiro-cli:latest chat --trust-all-tools ;;
        10) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.qwen:/home/node/.qwen" qwen-code:latest --yolo ;;
        *) echo "Invalid selection" ; exit 1 ;;
    esac
}

update_agent() {
    echo "Available AI Agents:"
    echo "1. claude-code"
    echo "2. codex-cli"
    echo "3. copilot-cli"
    echo "4. codespeak"
    echo "5. devstral-cli"
    echo "6. gemini-cli"
    echo "7. junie-cli"
    echo "8. kimi-cli"
    echo "9. kiro-cli"
    echo "10. qwen-code"

    read -rp "Select agent to update (1-10): " choice

    case "$choice" in
        1)  IMAGE="claude-code:latest"
            HINT="npm install -g @anthropic-ai/claude-code@latest" ;;
        2)  IMAGE="codex-cli:latest"
            HINT="npm install -g @openai/codex@latest" ;;
        3)  IMAGE="copilot-cli:latest"
            HINT="npm install -g @github/copilot@latest" ;;
        4)  IMAGE="codespeak:latest"
            HINT="uv tool install --force codespeak-cli" ;;
        5)  IMAGE="devstral-cli:latest"
            HINT="uv tool install --force mistral-vibe" ;;
        6)  IMAGE="gemini-cli:latest"
            HINT="npm install -g @google/gemini-cli@latest" ;;
        7)  IMAGE="junie-cli:latest"
            HINT="curl -fsSL https://junie.jetbrains.com/install.sh | bash" ;;
        8)  IMAGE="kimi-cli:latest"
            HINT="uv tool install --force --python 3.13 kimi-cli" ;;
        9)  IMAGE="kiro-cli:latest"
            HINT="curl -fsSL https://cli.kiro.dev/install | bash" ;;
        10) IMAGE="qwen-code:latest"
            HINT="npm install -g @qwen-code/qwen-code@latest" ;;
        *)  echo "Invalid selection" ; exit 1 ;;
    esac

    CONTAINER_NAME="update-${IMAGE%%:*}-$$"
    echo "Hint: $HINT"
    execute sudo docker run -it --user root --entrypoint /bin/bash --name "$CONTAINER_NAME" "$IMAGE"

    if sudo docker inspect "$CONTAINER_NAME" > /dev/null 2>&1; then
        echo "Committing changes to $IMAGE ..."
        execute sudo docker commit "$CONTAINER_NAME" "$IMAGE"
        execute sudo docker rm "$CONTAINER_NAME"
    else
        echo "Container was not created; nothing to commit."
    fi
}

build_agent() {
    echo "Available AI Agents:"
    echo "1. claude-code"
    echo "2. codex-cli"
    echo "3. copilot-cli"
    echo "4. codespeak"
    echo "5. devstral-cli"
    echo "6. gemini-cli"
    echo "7. junie-cli"
    echo "8. kimi-cli"
    echo "9. kiro-cli"
    echo "10. qwen-code"

    read -rp "Select agent to build (1-10): " choice

    case "$choice" in
        1) execute docker build --no-cache -t claude-code:latest agents/claude-code ;;
        2) execute docker build --no-cache -t codex-cli:latest agents/codex-cli ;;
        3) execute docker build --no-cache -t copilot-cli:latest agents/copilot-cli ;;
        4) execute docker build --no-cache -t codespeak:latest agents/codespeak ;;
        5) execute docker build --no-cache -t devstral-cli:latest agents/devstral-cli ;;
        6) execute docker build --no-cache -t gemini-cli:latest agents/gemini-cli ;;
        7) execute docker build --no-cache -t junie-cli:latest agents/junie-cli ;;
        8) execute docker build --no-cache -t kimi-cli:latest agents/kimi-cli ;;
        9) execute docker build --no-cache -t kiro-cli:latest agents/kiro-cli ;;
        10) execute docker build --no-cache -t qwen-code:latest agents/qwen-code ;;
        *) echo "Unknown agent" ; exit 1 ;;
    esac
}

usage() {
    echo "Usage: $0 <run|build|update> [args...]"
    echo ""
    echo "Commands:"
    echo "  run    Select and run an agent container (default)"
    echo "  build  Build an agent Docker image"
    echo "  update Drop into a root shell to update an agent, then commit changes"
    exit 1
}

case "$1" in
    run|"")  run_agent ;;
    build)   build_agent ;;
    update)  update_agent ;;
    *)       usage ;;
esac
