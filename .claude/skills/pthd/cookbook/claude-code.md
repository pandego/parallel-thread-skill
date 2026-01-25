# Purpose

Command template for Claude Code agent processes in pthd.

## Variables

COMMAND_TEMPLATE: claude --dangerously-skip-permissions '{prompt}'

## Instructions

- Before first use, run `claude --help` to understand options
- Interactive mode (no `-p` flag) - prompt as positional argument
- `--dangerously-skip-permissions` enables autonomous operation (no approval prompts)
- Aliases: cc, claude, claude-code
