# Purpose

Command template for Claude Code agent processes in pthd.

## Variables

DEFAULT_MODEL: sonnet
HEAVY_MODEL: opus
BASE_MODEL: sonnet
FAST_MODEL: haiku

## Instructions

- Before first use, run `claude --help` to understand options
- Always use interactive mode (no `-p` flag) - prompt as positional argument
- For the --model argument, use the DEFAULT_MODEL. pthd does not currently support model selection per-agent.
- Always run with `--dangerously-skip-permissions` for autonomous operation (no approval prompts)
- Aliases: cc, claude, claude-code
