#!/bin/bash

execute() {
    echo -e "\033[1;34m[EXECUTING]\033[0m: $*"
    "$@"
}

run_agent() {
    echo "Available AI Agents:"
    # BEGIN GENERATED RUN MENU
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
    echo "11. opencode-cli"
    echo "12. pi-coding-agent"
    echo "13. cursor-cli"
# END GENERATED RUN MENU
    # BEGIN GENERATED AGENT COUNT
AGENT_COUNT=13
# END GENERATED AGENT COUNT

    read -rp "Select agent (1-${AGENT_COUNT}): " choice

    case "$choice" in
        # BEGIN GENERATED RUN CASE
        1) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.claude:/home/ubuntu/.claude" -v "$HOME/.claude/.claude.json:/home/ubuntu/.claude.json" -e ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" claude-code:latest --verbose --dangerously-skip-permissions ;;
        2) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.codex:/home/node/.codex" -e OPENAI_API_KEY="${OPENAI_API_KEY}" codex-cli:latest -a never --sandbox danger-full-access ;;
        3) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.copilot:/home/node/.copilot" -e COPILOT_GITHUB_TOKEN="${COPILOT_GITHUB_TOKEN}" copilot-cli:latest --allow-all ;;
        4) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.codespeak:/home/codespeak/.codespeak" -e ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" --entrypoint /bin/bash codespeak:latest ;;
        5) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.vibe:/root/.vibe" -e MISTRAL_API_KEY="${MISTRAL_API_KEY}" devstral-cli:latest --agent=auto-approve ;;
        6) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.gemini:/home/node/.gemini" -e GEMINI_API_KEY="${GEMINI_API_KEY}" gemini-cli:latest --approval-mode=yolo ;;
        7) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.junie:/home/ubuntu/.junie" -e JUNIE_API_KEY="${JUNIE_API_KEY}" junie-cli:latest --brave ;;
        8) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.kimi:/home/appuser/.kimi" kimi-cli:latest --yolo ;;
        9) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.kiro:/home/ubuntu/.kiro" -v "$HOME/.local/share/kiro-cli:/home/ubuntu/.local/share/kiro-cli" kiro-cli:latest chat --trust-all-tools ;;
        10) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.qwen:/home/node/.qwen" qwen-code:latest --yolo ;;
        11) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.opencode:/home/node/.opencode" opencode-cli:latest ;;
        12) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.pi:/home/node/.pi" pi-coding-agent:latest ;;
        13) execute sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.cursor:/home/ubuntu/.cursor" -v "$HOME/.config/cursor:/home/ubuntu/.config/cursor" cursor-cli:latest --sandbox disabled --yolo ;;
        *) echo "Invalid selection" ; exit 1 ;;
# END GENERATED RUN CASE
    esac
}

build_agent() {
    echo "Available AI Agents:"
    # BEGIN GENERATED BUILD MENU
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
    echo "11. opencode-cli"
    echo "12. pi-coding-agent"
    echo "13. cursor-cli"
# END GENERATED BUILD MENU

    read -rp "Select agent to build (1-${AGENT_COUNT}): " choice

    case "$choice" in
        # BEGIN GENERATED BUILD CASE
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
        11) execute docker build --no-cache -t opencode-cli:latest agents/opencode-cli ;;
        12) execute docker build --no-cache -t pi-coding-agent:latest agents/pi-coding-agent ;;
        13) execute docker build --no-cache -t cursor-cli:latest agents/cursor-cli ;;
        *) echo "Unknown agent" ; exit 1 ;;
# END GENERATED BUILD CASE
    esac
}

rebuild_all() {
    echo "Rebuilding all agent images..."
    local failed=()
    local succeeded=()

    # BEGIN GENERATED REBUILD ALL CASE
    echo "[1/13] claude-code"
    execute docker build --no-cache -t claude-code:latest agents/claude-code && succeeded+=("claude-code") || failed+=("claude-code")
    echo "[2/13] codex-cli"
    execute docker build --no-cache -t codex-cli:latest agents/codex-cli && succeeded+=("codex-cli") || failed+=("codex-cli")
    echo "[3/13] copilot-cli"
    execute docker build --no-cache -t copilot-cli:latest agents/copilot-cli && succeeded+=("copilot-cli") || failed+=("copilot-cli")
    echo "[4/13] codespeak"
    execute docker build --no-cache -t codespeak:latest agents/codespeak && succeeded+=("codespeak") || failed+=("codespeak")
    echo "[5/13] devstral-cli"
    execute docker build --no-cache -t devstral-cli:latest agents/devstral-cli && succeeded+=("devstral-cli") || failed+=("devstral-cli")
    echo "[6/13] gemini-cli"
    execute docker build --no-cache -t gemini-cli:latest agents/gemini-cli && succeeded+=("gemini-cli") || failed+=("gemini-cli")
    echo "[7/13] junie-cli"
    execute docker build --no-cache -t junie-cli:latest agents/junie-cli && succeeded+=("junie-cli") || failed+=("junie-cli")
    echo "[8/13] kimi-cli"
    execute docker build --no-cache -t kimi-cli:latest agents/kimi-cli && succeeded+=("kimi-cli") || failed+=("kimi-cli")
    echo "[9/13] kiro-cli"
    execute docker build --no-cache -t kiro-cli:latest agents/kiro-cli && succeeded+=("kiro-cli") || failed+=("kiro-cli")
    echo "[10/13] qwen-code"
    execute docker build --no-cache -t qwen-code:latest agents/qwen-code && succeeded+=("qwen-code") || failed+=("qwen-code")
    echo "[11/13] opencode-cli"
    execute docker build --no-cache -t opencode-cli:latest agents/opencode-cli && succeeded+=("opencode-cli") || failed+=("opencode-cli")
    echo "[12/13] pi-coding-agent"
    execute docker build --no-cache -t pi-coding-agent:latest agents/pi-coding-agent && succeeded+=("pi-coding-agent") || failed+=("pi-coding-agent")
    echo "[13/13] cursor-cli"
    execute docker build --no-cache -t cursor-cli:latest agents/cursor-cli && succeeded+=("cursor-cli") || failed+=("cursor-cli")
# END GENERATED REBUILD ALL CASE

    echo ""
    echo -e "\033[1;32m[DONE]\033[0m Rebuild complete."
    echo "  Succeeded (${#succeeded[@]}): ${succeeded[*]:-none}"
    if [ ${#failed[@]} -gt 0 ]; then
        echo -e "  \033[1;31mFailed    (${#failed[@]}): ${failed[*]}\033[0m"
        exit 1
    fi
}

usage() {
    echo "Usage: $0 <run|build|rebuild-all> [args...]"
    echo ""
    echo "Commands:"
    echo "  run         Select and run an agent container (default)"
    echo "  build       Build a single agent Docker image"
    echo "  rebuild-all Rebuild ALL agent Docker images sequentially"
    exit 1
}

case "$1" in
    run|"")       run_agent ;;
    build)        build_agent ;;
    rebuild-all)  rebuild_all ;;
    *)            usage ;;
esac
