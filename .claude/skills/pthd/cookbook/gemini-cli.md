# Purpose

Command template for Gemini CLI agent processes in pthd.

## Variables

DEFAULT_MODEL: gemini-3-pro-preview
HEAVY_MODEL: gemini-3-pro-preview
BASE_MODEL: gemini-3-pro-preview
FAST_MODEL: gemini-3-flash

## Instructions

- Before first use, run `gemini --help` to understand options
- Always use interactive mode with `-i` flag as the last flag, right before the prompt
- For the --model argument, use the DEFAULT_MODEL. pthd does not currently support model selection per-agent.
- Always run with `-y` (yolo mode) for autonomous operation (no approval prompts)
- Aliases: gem, gems, gemini, gemini-cli
