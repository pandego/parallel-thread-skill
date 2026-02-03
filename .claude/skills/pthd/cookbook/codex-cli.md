# Purpose

Command template for Codex CLI agent processes in pthd.

## Variables

DEFAULT_MODEL: gpt-5.2-codex
HEAVY_MODEL: gpt-5.1-codex-max
BASE_MODEL: gpt-5.2
FAST_MODEL: gpt-5.1-codex-mini

## Instructions

- Before first use, run `codex --help` to understand options
- Always use interactive mode (no `-p` flag) - prompt as positional argument
- For the -m (model) argument, use the DEFAULT_MODEL. pthd does not currently support model selection per-agent.
- Always run with `--dangerously-bypass-approvals-and-sandbox` for autonomous operation
- Aliases: codex, codex-cli
