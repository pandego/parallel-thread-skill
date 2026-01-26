---
name: pthd (Parallel Terminal Hydra)
description: Spawn multiple parallel agent processes using mprocs. Use when user wants to run the same prompt across multiple agents simultaneously.
---

# Purpose

Spawn multiple parallel agent instances using mprocs. Each agent runs the same prompt in its own terminal pane.

## Variables

ENABLE_CLAUDE_CODE: true
ENABLE_GEMINI_CLI: true
ENABLE_CODEX_CLI: true
TOOL_ALIASES:
  cc: claude-code
  gem: gemini-cli
  codex: codex-cli

## Instructions

Parse the user's request to extract:
1. **Prompt**: The task/prompt to run on all agents
2. **Tool specification**: Which tools and how many instances

### Tool Specification Formats

- `3 cc, 3 gem, 3 codex` - Explicit count per tool
- `cc 2, gem 1` - Alternate syntax
- `4` - Single number means all enabled tools with that count

### Agent Name Placeholder

Use `{{AGENT}}` in your prompt to get it replaced with the unique agent name for each process:
- `cc-1`, `cc-2`, `cc-3` for Claude Code instances
- `gem-1`, `gem-2`, `gem-3` for Gemini CLI instances
- `codex-1`, `codex-2`, `codex-3` for Codex CLI instances

**Example**: If the user says "save to `./tmp/{{AGENT}}_response.md`", each agent will save to a unique file:
- cc-1 saves to `./tmp/cc-1_response.md`
- gem-1 saves to `./tmp/gem-1_response.md`
- codex-2 saves to `./tmp/codex-2_response.md`

**IMPORTANT**: When the user's prompt mentions saving files with dynamic agent names (like `<agent>`, `$agent`, or similar patterns), automatically convert them to use `{{AGENT}}`.

## Workflow

1. Parse the user request for prompt and tool specification
2. READ: `.claude/skills/pthd/tools/pthd.py` to understand the implementation
3. READ the relevant cookbooks for each enabled tool to get command templates
4. (First time only) Run `claude --help`, `gemini --help`, `codex --help` to understand CLI options
5. Execute `pthd.py` to generate the mprocs config
6. Use fork-terminal skill to launch: `mprocs -c /tmp/pthd/<slug>.yml`

## Cookbook

### Claude Code Instances

- IF: User specifies `cc` instances AND `ENABLE_CLAUDE_CODE` is true
- THEN: Read `.claude/skills/pthd/cookbook/claude-code.md` for command template
- EXAMPLES:
  - "pthd 3 cc: build a todo app"
  - "spawn 2 claude agents for: refactor this code"

### Gemini CLI Instances

- IF: User specifies `gem` instances AND `ENABLE_GEMINI_CLI` is true
- THEN: Read `.claude/skills/pthd/cookbook/gemini-cli.md` for command template
- EXAMPLES:
  - "pthd 3 gem: analyze this codebase"
  - "run gemini 2x on: explain this function"

### Codex CLI Instances

- IF: User specifies `codex` instances AND `ENABLE_CODEX_CLI` is true
- THEN: Read `.claude/skills/pthd/cookbook/codex-cli.md` for command template
- EXAMPLES:
  - "pthd 3 codex: write unit tests"
  - "codex x2: implement feature X"
