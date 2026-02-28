#!/bin/bash

run_agent() {
    echo "Available AI Agents:"
    echo "1. claude-code"
    echo "2. codex-cli"
    echo "3. copilot-cli"
    echo "4. codespeak"
    echo "5. devstral-cli"
    echo "6. gemini-cli"
    echo "7. kimi-cli"
    echo "8. kiro-cli"
    echo "9. qwen-code"

    read -rp "Select agent (1-9): " choice

    case "$choice" in
        1) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.claude:/home/node/.claude" -v "$HOME/.claude/.claude.json:/home/node/.claude.json" -e ANTHROPIC_API_KEY claude-code:latest --verbose --dangerously-skip-permissions ;;
        2) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.codex:/home/node/.codex" -e OPENAI_API_KEY codex-cli:latest -a never ;;
        3) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.copilot:/home/node/.copilot" copilot-cli:latest --allow-all ;;
        4) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.codespeak:/home/codespeak/.codespeak" -e ANTHROPIC_API_KEY codespeak:latest ;;
        5) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.vibe:/home/appuser/.vibe" -e MISTRAL_API_KEY devstral-cli:latest ;;
        6) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.gemini:/home/node/.gemini" -e GEMINI_API_KEY gemini-cli:latest --approval-mode=yolo ;;
        7) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.kimi:/home/appuser/.kimi" kimi-cli:latest ;;
        8) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.kiro:/home/ubuntu/.kiro" -v "$HOME/.local/share/kiro-cli:/home/ubuntu/.local/share/kiro-cli" kiro-cli:latest chat --trust-all-tools ;;
        9) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.qwen:/home/node/.qwen" qwen-code:latest --yolo ;;
        *) echo "Invalid selection" ; exit 1 ;;
    esac
}

build_agent() {
    echo "Available AI Agents:"
    echo "1. claude-code"
    echo "2. codex-cli"
    echo "3. copilot-cli"
    echo "4. codespeak"
    echo "5. devstral-cli"
    echo "6. gemini-cli"
    echo "7. kimi-cli"
    echo "8. kiro-cli"
    echo "9. qwen-code"

    read -rp "Select agent to build (1-9): " choice

    case "$choice" in
        1) docker build --no-cache -t claude-code:latest agents/claude-code ;;
        2) docker build --no-cache -t codex-cli:latest agents/codex-cli ;;
        3) docker build --no-cache -t copilot-cli:latest agents/copilot-cli ;;
        4) docker build --no-cache -t codespeak:latest agents/codespeak ;;
        5) docker build --no-cache -t devstral-cli:latest agents/devstral-cli ;;
        6) docker build --no-cache -t gemini-cli:latest agents/gemini-cli ;;
        7) docker build --no-cache -t kimi-cli:latest agents/kimi-cli ;;
        8) docker build --no-cache -t kiro-cli:latest agents/kiro-cli ;;
        9) docker build --no-cache -t qwen-code:latest agents/qwen-code ;;
        *) echo "Unknown agent" ; exit 1 ;;
    esac
}

usage() {
    echo "Usage: $0 <run|build> [args...]"
    echo ""
    echo "Commands:"
    echo "  run    Select and run an agent container (default)"
    echo "  build  Build an agent Docker image"
    exit 1
}

case "$1" in
    run|"")  run_agent ;;
    build)   build_agent ;;
    *)       usage ;;
esac
