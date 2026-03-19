#!/usr/bin/env python3
import json
import re
import shlex
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "agents.json"
README_PATH = ROOT / "README.md"
AGENT_SH_PATH = ROOT / "agent.sh"


def load_agents():
    with MANIFEST_PATH.open() as f:
        data = json.load(f)
    return data["agents"]


def replace_section(text, start_marker, end_marker, body, file_label):
    try:
        start = text.index(start_marker) + len(start_marker)
    except ValueError as exc:
        raise ValueError(f"Missing start marker '{start_marker}' in {file_label}") from exc

    try:
        end = text.index(end_marker)
    except ValueError as exc:
        raise ValueError(f"Missing end marker '{end_marker}' in {file_label}") from exc

    if end < start:
        raise ValueError(
            f"Marker order invalid in {file_label}: '{end_marker}' appears before '{start_marker}'"
        )

    return text[:start] + "\n" + body.rstrip() + "\n" + text[end:]


def validate_agents(agents):
    safe_id = re.compile(r"^[a-z0-9][a-z0-9-]*$")
    safe_image_dir = re.compile(r"^agents/[a-z0-9][a-z0-9-]*$")
    safe_env = re.compile(r"^[A-Z_][A-Z0-9_]*$")

    for agent in agents:
        agent_id = agent["id"]
        if not safe_id.match(agent_id):
            raise ValueError(f"Invalid agent id '{agent_id}' in {MANIFEST_PATH.name}")

        image_dir = agent["image_dir"]
        if not safe_image_dir.match(image_dir):
            raise ValueError(
                f"Invalid image_dir '{image_dir}' for agent '{agent_id}' in {MANIFEST_PATH.name}"
            )

        for env_var in agent["run"]["env_vars"]:
            if not safe_env.match(env_var):
                raise ValueError(
                    f"Invalid env var name '{env_var}' for agent '{agent_id}' in {MANIFEST_PATH.name}"
                )


def render_root_table(agents):
    lines = [
        "| Directory | CLI | Provider | Base Image | Non-Root |",
        "|-----------|-----|----------|------------|-----------|",
    ]
    for agent in agents:
        non_root = "Yes" if agent["non_root"] else "No"
        lines.append(
            f"| [{agent['id']}](./{agent['image_dir']}/) | {agent['display_name']} | "
            f"{agent['provider']} | {agent['base_image']} | {non_root} |"
        )
    return "\n".join(lines)


def render_menu_lines(agents, indent):
    return "\n".join(
        f'{indent}echo "{index}. {agent["id"]}"'
        for index, agent in enumerate(agents, start=1)
    )


def render_agent_count(agents):
    return f"AGENT_COUNT={len(agents)}"


def render_run_case(agents):
    lines = []
    for index, agent in enumerate(agents, start=1):
        parts = ['execute sudo docker run --rm -it -v "$(pwd):/app"']
        for mount in agent["run"]["mounts"]:
            mount_value = f'{mount["host"]}:{mount["container"]}'
            # Use double quotes for mounts to allow variable expansion
            parts.append(f'-v "{mount_value}"')
        for env_var in agent["run"]["env_vars"]:
            parts.append(f"-e {env_var}=\"${{{env_var}}}\"")
        parts.extend(shlex.quote(arg) for arg in agent["run"]["docker_args"])
        parts.append(shlex.quote(f'{agent["id"]}:latest'))
        parts.extend(shlex.quote(arg) for arg in agent["run"]["command_args"])
        lines.append(f"        {index}) {' '.join(parts)} ;;")
    lines.append('        *) echo "Invalid selection" ; exit 1 ;;')
    return "\n".join(lines)


def render_update_case(agents):
    lines = []
    for index, agent in enumerate(agents, start=1):
        lines.append(f'        {index})  IMAGE="{agent["id"]}:latest"')
        lines.append(f'            HINT="{agent["update_hint"]}" ;;')
    lines.append('        *)  echo "Invalid selection" ; exit 1 ;;')
    return "\n".join(lines)


def render_build_case(agents):
    lines = []
    for index, agent in enumerate(agents, start=1):
        lines.append(
            f"        {index}) execute docker build --no-cache -t {agent['id']}:latest {agent['image_dir']} ;;"
        )
    lines.append('        *) echo "Unknown agent" ; exit 1 ;;')
    return "\n".join(lines)


def sync_readme(agents):
    text = README_PATH.read_text()
    updated = replace_section(
        text,
        "<!-- BEGIN GENERATED INCLUDED CLIS -->",
        "<!-- END GENERATED INCLUDED CLIS -->",
        render_root_table(agents),
        README_PATH,
    )
    README_PATH.write_text(updated)


def sync_agent_sh(agents):
    text = AGENT_SH_PATH.read_text()
    updated = text
    updated = replace_section(
        updated,
        "# BEGIN GENERATED RUN MENU",
        "# END GENERATED RUN MENU",
        render_menu_lines(agents, "    "),
        AGENT_SH_PATH,
    )
    updated = replace_section(
        updated,
        "# BEGIN GENERATED AGENT COUNT",
        "# END GENERATED AGENT COUNT",
        render_agent_count(agents),
        AGENT_SH_PATH,
    )
    updated = replace_section(
        updated,
        "# BEGIN GENERATED RUN CASE",
        "# END GENERATED RUN CASE",
        render_run_case(agents),
        AGENT_SH_PATH,
    )
    updated = replace_section(
        updated,
        "# BEGIN GENERATED UPDATE MENU",
        "# END GENERATED UPDATE MENU",
        render_menu_lines(agents, "    "),
        AGENT_SH_PATH,
    )
    updated = replace_section(
        updated,
        "# BEGIN GENERATED UPDATE CASE",
        "# END GENERATED UPDATE CASE",
        render_update_case(agents),
        AGENT_SH_PATH,
    )
    updated = replace_section(
        updated,
        "# BEGIN GENERATED BUILD MENU",
        "# END GENERATED BUILD MENU",
        render_menu_lines(agents, "    "),
        AGENT_SH_PATH,
    )
    updated = replace_section(
        updated,
        "# BEGIN GENERATED BUILD CASE",
        "# END GENERATED BUILD CASE",
        render_build_case(agents),
        AGENT_SH_PATH,
    )
    AGENT_SH_PATH.write_text(updated)


def main():
    agents = load_agents()
    validate_agents(agents)
    sync_readme(agents)
    sync_agent_sh(agents)
    print(f"Synced metadata for {len(agents)} agents in README.md and agent.sh")


if __name__ == "__main__":
    main()
