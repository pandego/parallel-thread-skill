# Purpose

Command template for OpenCode agent processes in pthd.

## Variables

DEFAULT_MODEL: opencode/kimi-k2.5-free
HEAVY_MODEL: opencode/glm-4.7-free
BASE_MODEL: opencode/minimax-m2.1-free
FAST_MODEL: opencode/big-pickle

## Instructions

- Before first use, run `opencode --help` to understand options
- Always use interactive mode by running `opencode` with the `--prompt` flag
- For the --model (-m) argument, use the DEFAULT_MODEL. pthd does not currently support model selection per-agent.
- OpenCode does not require permission bypass flags - it runs interactively by default
- Aliases: oc, opencode, open-code, open code
