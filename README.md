# Parallel Thread Skill (pthd)

A Claude Code skill that spawns multiple parallel AI agent processes using [mprocs](https://github.com/pvolok/mprocs). Run the same prompt across multiple agents simultaneously, each in its own terminal pane.

<img src="images/parallel-thread.png" alt="Parallel Thread Skill" width="800">

## What is a Claude Code Skill?

A **skill** is a modular, context-aware capability that Claude Code can automatically discover and invoke based on natural language requests. Unlike slash commands (which require explicit invocation), skills are triggered when Claude recognizes that your request matches the skill's purpose.

This skill is designed to work alongside the [fork-terminal](https://github.com/IndyDevDan/fork-terminal-skill) skill, which handles spawning new terminal windows.

## How It Works: pthd + fork-terminal Synergy

The parallel-thread-skill works in conjunction with fork-terminal:

```
User Request
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│  pthd (this skill)                                          │
│  1. Parse tool specification (which agents, how many)       │
│  2. Generate mprocs YAML config                             │
│  3. Write config to /tmp/pthd/<slug>.yml                    │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│  fork-terminal skill                                        │
│  1. Open new terminal window                                │
│  2. Execute: mprocs -c /tmp/pthd/<slug>.yml                 │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│  mprocs                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                     │
│  │  cc-1    │ │  cc-2    │ │  gem-1   │  ...                │
│  │ (Claude) │ │ (Claude) │ │ (Gemini) │                     │
│  └──────────┘ └──────────┘ └──────────┘                     │
│  All agents running the same prompt in parallel             │
└─────────────────────────────────────────────────────────────┘
```

## Supported Tools

| Tool | Aliases | Autonomy Flag |
|------|---------|---------------|
| **Claude Code** | `cc`, `claude`, `claude-code` | `--dangerously-skip-permissions` |
| **Gemini CLI** | `gem`, `gems`, `gemini`, `gemini-cli` | `-y` (yolo mode) |
| **Codex CLI** | `codex`, `codex-cli` | `--dangerously-bypass-approvals-and-sandbox` |

All agents run in **autonomous mode** to prevent approval prompts from blocking parallel execution.

## Usage Examples

### Basic: Single Tool Type

```
pthd 3 cc: build a todo app
```
Spawns 3 Claude Code agents, all working on "build a todo app".

### Mixed: Multiple Tool Types

```
pthd 2 cc, 2 gem, 1 codex: refactor this codebase
```
Spawns 2 Claude + 2 Gemini + 1 Codex agents in parallel.

### All Tools: Single Number

```
pthd 4: analyze security vulnerabilities
```
Spawns 4 instances of **each** enabled tool (12 total agents).

### Alternate Syntax

```
spawn 2 claude agents for: write unit tests
run gemini 3x on: explain this function
codex x2: implement the login feature
```

## Tool Specification Formats

The skill accepts flexible input formats:

| Format | Example | Result |
|--------|---------|--------|
| Count + alias | `3 cc` | 3 Claude Code |
| Alias + count | `gem 2` | 2 Gemini CLI |
| Comma-separated | `2 cc, 3 gem` | 2 Claude + 3 Gemini |
| Single number | `4` | 4 of each enabled tool |
| Natural language | `2 claude agents` | 2 Claude Code |

## Requirements

- **mprocs**: Terminal multiplexer - [installation guide](https://github.com/pvolok/mprocs#installation)
- **uv**: Python package manager - [installation guide](https://docs.astral.sh/uv/getting-started/installation/)
- **fork-terminal skill**: For spawning the terminal window
- At least one of the supported AI CLI tools installed:
  - [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
  - [Gemini CLI](https://github.com/google-gemini/gemini-cli)
  - [Codex CLI](https://github.com/openai/codex)

## Installation

Copy the `.claude/skills/pthd/` directory to your project's `.claude/skills/` folder, or to `~/.claude/skills/` for personal use across all projects.

Ensure you also have:

1. The [fork-terminal skill](https://github.com/IndyDevDan/fork-terminal-skill) installed.

2. **mprocs** installed:
   ```bash
   # macOS
   brew install mprocs

   # Linux (cargo)
   cargo install mprocs

   # Or download from releases
   ```

## Architecture

```
parallel-thread-skill/
├── README.md
├── .gitignore
├── images/
│   └── pthd-demo.png
└── .claude/
    └── skills/
        └── pthd/
            ├── SKILL.md          # Skill definition & workflow
            ├── cookbook/
            │   ├── claude-code.md    # Claude Code command template
            │   ├── codex-cli.md      # Codex CLI command template
            │   └── gemini-cli.md     # Gemini CLI command template
            └── tools/
                └── pthd.py       # Core implementation
```

## Configuration

Enable/disable tools in `.claude/skills/pthd/SKILL.md`:

```yaml
ENABLE_CLAUDE_CODE: true
ENABLE_GEMINI_CLI: true
ENABLE_CODEX_CLI: true
```

## How the Config Generation Works

When you invoke pthd, it:

1. **Parses** your tool specification (e.g., `3 cc, 2 gem`)
2. **Generates** a YAML config for mprocs:
   ```yaml
   procs:
     cc-1:
       shell: claude --dangerously-skip-permissions 'your prompt'
     cc-2:
       shell: claude --dangerously-skip-permissions 'your prompt'
     cc-3:
       shell: claude --dangerously-skip-permissions 'your prompt'
     gem-1:
       shell: gemini -y -i 'your prompt'
     gem-2:
       shell: gemini -y -i 'your prompt'
   ```
3. **Writes** the config to `/tmp/pthd/<slug>.yml`
4. **Returns** the mprocs launch command

## Platform Support

Works on any platform supported by mprocs and fork-terminal:
- **macOS** (Terminal.app)
- **Windows** (cmd)
- **Linux** (gnome-terminal, konsole, xterm)

## Credits

Inspired by [IndyDevDan](https://github.com/IndyDevDan) after seeing this skill in action in one of his videos. Unable to find it open-sourced, I reverse-engineered the implementation based on the demonstrated functionality.
