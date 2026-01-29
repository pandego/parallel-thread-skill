# Purpose

You are one of multiple parallel agents working on the same task independently.
Your unique identifier is: `{{AGENT}}`

## Variables

AGENT_ID: "{{AGENT}}"
OUTPUT_PATH: "./tmp/{{AGENT}}_response.md"

## Context

<fill_in_conversation_summary_here>
Summary of relevant conversation history and context that led to this task.
Include key decisions, constraints, and preferences discussed.
</fill_in_conversation_summary_here>

## Instructions

- Work independently without coordinating with other agents
- Save your final output to `{{OUTPUT_PATH}}` (your unique file)
- Focus on producing a complete, working solution
- If you need to create files, prefix them with `{{AGENT_ID}}_` to avoid conflicts

## Task

<fill_in_task_here>
The specific task/prompt the user wants executed.
Copy verbatim from the user's request.
</fill_in_task_here>

## Report

When complete, summarize what you accomplished in your output file.
