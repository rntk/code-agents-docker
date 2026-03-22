#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
AGENT_SH = ROOT / "agent.sh"
AGENTS_DIR = ROOT / "agents"


def execute(cmd, **kwargs):
    print(f"\033[1;34m[EXECUTING]\033[0m: {cmd}")
    return subprocess.run(cmd, shell=True, **kwargs)


def build_agent(name):
    agent_dir = AGENTS_DIR / name
    if not agent_dir.is_dir():
        print(f"Agent '{name}' not found in agents/")
        sys.exit(1)
    if not (agent_dir / "Dockerfile").exists():
        print(f"Dockerfile not found in {agent_dir}/")
        sys.exit(1)
    result = execute(f"docker build --no-cache -t {name}:latest {agent_dir}")
    sys.exit(result.returncode)


def build_all():
    agents = sorted(
        d for d in AGENTS_DIR.iterdir()
        if d.is_dir() and (d / "Dockerfile").exists()
    )
    if not agents:
        print("No agents found.")
        sys.exit(1)

    failed = []
    succeeded = []
    for i, agent_dir in enumerate(agents, 1):
        name = agent_dir.name
        print(f"\n[{i}/{len(agents)}] {name}")
        result = execute(f"docker build --no-cache -t {name}:latest {agent_dir}")
        if result.returncode == 0:
            succeeded.append(name)
        else:
            failed.append(name)

    print()
    print(f"\033[1;32m[DONE]\033[0m Build complete.")
    print(f"  Succeeded ({len(succeeded)}): {', '.join(succeeded) or 'none'}")
    if failed:
        print(f"  \033[1;31mFailed    ({len(failed)}): {', '.join(failed)}\033[0m")
        sys.exit(1)


def run_agent():
    result = execute(f"bash {AGENT_SH} run")
    sys.exit(result.returncode)


def update_agent():
    result = execute(f"bash {AGENT_SH} update")
    sys.exit(result.returncode)


def sync_metadata():
    result = execute(f"python3 {ROOT / 'scripts' / 'sync_agents.py'}")
    sys.exit(result.returncode)


def generate_prompt():
    result = execute(f"python3 {ROOT / 'scripts' / 'generate_prompt.py'}")
    sys.exit(result.returncode)


def clean():
    result = execute("docker image prune -f")
    sys.exit(result.returncode)


def usage():
    print("Usage: python scripts/make.py <command> [args...]")
    print()
    print("Commands:")
    print("  build-all          Build all agent Docker images")
    print("  build <agent>      Build a single agent Docker image")
    print("  run                Select and run an agent container")
    print("  update             Drop into a root shell to update an agent, then commit")
    print("  sync-metadata      Sync agent.sh and README.md from agents.json")
    print("  generate-prompt    Generate a project-specific Dockerfile prompt")
    print("  clean              Remove dangling Docker images")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        usage()

    cmd = sys.argv[1]

    if cmd == "build-all":
        build_all()
    elif cmd == "build":
        if len(sys.argv) < 3:
            print("Usage: python scripts/make.py build <agent-name>")
            sys.exit(1)
        build_agent(sys.argv[2])
    elif cmd == "run":
        run_agent()
    elif cmd == "update":
        update_agent()
    elif cmd == "sync-metadata":
        sync_metadata()
    elif cmd == "generate-prompt":
        generate_prompt()
    elif cmd == "clean":
        clean()
    else:
        print(f"Unknown command: {cmd}")
        usage()


if __name__ == "__main__":
    main()
