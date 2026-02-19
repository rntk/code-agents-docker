#!/bin/bash

echo "Available AI Agents:"
echo "1. claude-code"
echo "2. codex-cli"
echo "3. copilot-cli"
echo "4. devstral-cli"
echo "5. gemini-cli"
echo "6. kimi-cli"
echo "7. kiro-cli"
echo "8. qwen-code"

read -rp "Select agent (1-8): " choice

case "$choice" in
    1) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.claude:/home/node/.claude" -v "$HOME/.claude/.claude.json:/home/node/.claude.json" -e ANTHROPIC_API_KEY claude-code:latest --verbose --dangerously-skip-permissions ;;
    2) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.codex:/home/node/.codex" -e OPENAI_API_KEY codex-cli:latest -a never ;;
    3) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.copilot:/home/node/.copilot" copilot-cli:latest --allow-all ;;
    4) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.vibe:/home/appuser/.vibe" -e MISTRAL_API_KEY devstral-cli:latest ;;
    5) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.gemini:/home/node/.gemini" -e GEMINI_API_KEY gemini-cli:latest --approval-mode=yolo ;;
    6) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.kimi:/home/appuser/.kimi" kimi-cli:latest ;;
    7) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.kiro:/home/ubuntu/.kiro" -v "$HOME/.local/share/kiro-cli:/home/ubuntu/.local/share/kiro-cli" kiro-cli:latest chat --trust-all-tools ;;
    8) sudo docker run --rm -it -v "$(pwd):/app" -v "$HOME/.qwen:/home/node/.qwen" qwen-code:latest --yolo ;;
    *) echo "Invalid selection" ; exit 1 ;;
esac
