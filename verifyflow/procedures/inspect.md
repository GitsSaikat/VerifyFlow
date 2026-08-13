# Inspection Procedure

## Goal

Build an evidence-based understanding of the task and current environment
before selecting a solution or changing state.

## Extract the contract

Identify:

- Requested outcome and required delivery location
- Required artifact names, formats, interfaces, or behavior
- Explicit constraints and prohibited actions
- Authoritative inputs and existing acceptance checks
- What would count as observable success

Do not infer requirements from a preferred implementation when the task states
a different desired outcome.

## Inspect boundedly

Inspect the smallest relevant area first:

1. Identify top-level files and likely entry points.
2. Locate task instructions, configuration, tests, schemas, and existing output.
3. Read the nearest relevant documentation and source before broad searching.
4. Inspect only the files necessary to decide the next action.

Use `scripts/summarize_state.py --path <path>` when a concise read-only summary
would reduce uncertainty. Do not recurse broadly when a specific filename,
error, test, or path already identifies the relevant area.

## Identify interfaces

Determine the interfaces that constrain correctness:

- Function signatures and callers
- Command-line arguments, input/output channels, and exit behavior
- File schemas, encodings, delimiters, and required fields
- Test assertions, validators, and consumer expectations
- Existing project naming, formatting, and dependency conventions

Read `references/formats.md` only when a format or schema is material.

## Establish a baseline

Before changing anything, observe the relevant current state: a focused test,
current artifact metadata, exact error output, or current interface behavior.
Run the narrowest safe check that answers the immediate question.

## Choose the next action

Proceed when the target outcome, source of truth, likely change surface,
verification method, and safety scope are sufficiently clear. If a material
uncertainty remains, inspect one more relevant source or ask a focused question.
Do not manufacture missing requirements.
