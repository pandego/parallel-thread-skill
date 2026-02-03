#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pyyaml"]
# ///
"""Parallel Terminal Hydra - spawn multiple agent processes via mprocs."""

import os
import re
import tempfile
import yaml
from pathlib import Path


def slugify(text: str) -> str:
    """Convert text to filesystem-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower())[:50].strip("-")


def build_procs(prompt: str, tools: dict[str, int]) -> dict:
    """
    Build mprocs process config.

    tools = {"cc": 3, "gem": 2, "codex": 1, "oc": 2}

    All tools run in interactive mode with autonomous flags and default models
    (aligned with fork-terminal cookbook patterns):
    - cc: --model sonnet --dangerously-skip-permissions
    - gem: --model gemini-3-pro-preview -y -i (interactive, right before prompt)
    - codex: -m gpt-5.1-codex-max --dangerously-bypass-approvals-and-sandbox
    - oc: --model opencode/kimi-k2.5-free --prompt

    Agent name placeholder:
    - Use {{AGENT}} in your prompt to get replaced with the agent name (e.g., cc-1, gem-2)
    - Example: "save to ./tmp/{{AGENT}}_response.md" becomes "./tmp/cc-1_response.md"

    Uses cmd: arrays instead of shell: strings for cross-platform compatibility
    (avoids OS-specific quoting issues with single vs double quotes).
    """
    AGENT_PLACEHOLDER = "{{AGENT}}"

    # Default models (aligned with cookbook Variables)
    DEFAULT_MODELS = {
        "cc": "sonnet",
        "gem": "gemini-3-pro-preview",
        "codex": "gpt-5.1-codex-max",
        "oc": "opencode/kimi-k2.5-free",
    }

    procs = {}
    for tool, count in tools.items():
        if tool not in ["cc", "gem", "codex", "oc"]:
            continue
        for i in range(1, count + 1):
            name = f"{tool}-{i}"
            # Replace {{AGENT}} placeholder with actual agent name
            agent_prompt = prompt.replace(AGENT_PLACEHOLDER, name)
            model = DEFAULT_MODELS[tool]

            if tool == "cc":
                proc = {
                    "cmd": [
                        "claude",
                        "--model",
                        model,
                        "--dangerously-skip-permissions",
                        agent_prompt,
                    ]
                }
            elif tool == "gem":
                proc = {
                    "cmd": ["gemini", "--model", model, "-y", "-i", agent_prompt]
                }
            elif tool == "codex":
                proc = {
                    "cmd": [
                        "codex",
                        "-m",
                        model,
                        "--dangerously-bypass-approvals-and-sandbox",
                        agent_prompt,
                    ]
                }
            elif tool == "oc":
                proc = {
                    "cmd": ["opencode", "--model", model, "--prompt", agent_prompt]
                }
            else:
                continue

            procs[name] = proc

    return {"procs": procs}


def pthd(prompt: str, tools: dict[str, int]) -> str:
    """
    Create mprocs config and return launch command.

    Args:
        prompt: The prompt to pass to all agents
        tools: Dict of tool -> instance count, e.g. {"cc": 3, "gem": 3}

    Returns:
        The mprocs command to execute
    """
    # Build config path using cross-platform temp directory
    slug = slugify(prompt)
    config_dir = Path(tempfile.gettempdir()) / "pthd"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / f"{slug}.yml"

    # Build and write config
    config = build_procs(prompt, tools)
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    return f"mprocs -c {config_path}"


def parse_tool_spec(spec: str) -> dict[str, int]:
    """
    Parse tool specification string.

    Aliases:
        cc, claude, claude-code, claude code -> cc (Claude Code)
        gem, gems, gemini, gemini-cli, gemini cli -> gem (Gemini CLI)
        codex, codex-cli, codex cli -> codex (Codex CLI)
        oc, opencode, open-code, open code -> oc (OpenCode)

    Examples:
        "3 cc, 3 gem, 3 codex, 3 oc" -> {"cc": 3, "gem": 3, "codex": 3, "oc": 3}
        "cc 2, gems 1" -> {"cc": 2, "gem": 1}
        "4" -> {"cc": 4, "gem": 4, "codex": 4, "oc": 4}  # all tools
    """
    # Normalize aliases (order matters - multi-word first for regex)
    ALIASES = {
        # Claude Code
        "claude code": "cc",
        "claude-code": "cc",
        "claude": "cc",
        "cc": "cc",
        # Gemini CLI
        "gemini cli": "gem",
        "gemini-cli": "gem",
        "gemini": "gem",
        "gems": "gem",
        "gem": "gem",
        # Codex CLI
        "codex cli": "codex",
        "codex-cli": "codex",
        "codex": "codex",
        # OpenCode
        "open code": "oc",
        "open-code": "oc",
        "opencode": "oc",
        "oc": "oc",
    }

    spec = spec.strip()

    # Single number = all tools with that count
    if spec.isdigit():
        n = int(spec)
        return {"cc": n, "gem": n, "codex": n, "oc": n}

    tools = {}
    # Build pattern with multi-word aliases first (greedy matching)
    sorted_aliases = sorted(ALIASES.keys(), key=len, reverse=True)
    alias_pattern = "|".join(re.escape(a) for a in sorted_aliases)

    patterns = [
        rf"(\d+)\s*({alias_pattern})",  # "3 cc" or "3 claude code"
        rf"({alias_pattern})\s*[:\s]\s*(\d+)",  # "cc 3" or "claude code:3"
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, spec, re.IGNORECASE):
            groups = match.groups()
            if groups[0].isdigit():
                count, alias = int(groups[0]), groups[1].lower()
            else:
                alias, count = groups[0].lower(), int(groups[1])
            canonical = ALIASES.get(alias, alias)
            tools[canonical] = count

    return tools


if __name__ == "__main__":
    import sys

    # Usage: pthd.py "<prompt>" "<tool_spec>"
    # Example: pthd.py "build a todo app" "3 cc, 2 gem"
    if len(sys.argv) >= 3:
        prompt = sys.argv[1]
        tool_spec = sys.argv[2]
        tools = parse_tool_spec(tool_spec)
        cmd = pthd(prompt, tools)
        print(cmd)
