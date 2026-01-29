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

Use `{{AGENT}}` in prompts - replaced with unique agent name (`cc-1`, `gem-2`, etc.).
When user mentions saving files with dynamic names (`<agent>`, `$agent`), convert to `{{AGENT}}`.

### Parallel Summary Prompts

- IF: The user requests parallel agents with summary context (e.g., "include summary", "with context").
- THEN:
  - Read `.claude/skills/pthd/prompts/parallel_agent_prompt.md` as a template.
  - Fill in `<fill_in_conversation_summary_here>` with relevant conversation history.
  - Fill in `<fill_in_task_here>` with the user's task verbatim.
  - Pass the filled prompt to each parallel agent.
  - IMPORTANT: Fill the template IN YOUR MEMORY, don't modify the file.
- EXAMPLES:
  - "pthd 3 cc: build a todo app, include summary"
  - "spawn agents with context: refactor this code"

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
