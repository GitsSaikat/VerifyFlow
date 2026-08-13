# Evidence-Based Troubleshooting

Load this reference only after an observed failure, mismatch, or unexpected
result.

## Failure loop

1. Preserve exact command, input scope, exit status, and error output.
2. Identify the earliest meaningful failure, not the noisiest downstream effect.
3. Form one narrow hypothesis from evidence.
4. Run the least invasive check that can distinguish that hypothesis.
5. Apply one targeted change.
6. Rerun the relevant validation.
7. Stop and reassess if the same failure persists.

Do not convert uncertainty into repeated retries, broad edits, or ungrounded
dependency changes.

## Path or workspace mismatch

Symptoms: file not found, wrong artifact changed, command works from another
working directory.

Checks: confirm current directory, use explicit paths, inspect exact filenames
and case sensitivity, and confirm required output location.

## Input or schema mismatch

Symptoms: parser errors, missing fields, type errors, unexpected empty output.

Checks: inspect a minimal representative input; compare it with schema or a
valid example; verify encoding, delimiter, required fields, and null/empty
semantics. Read `formats.md` if structured data is involved.

## Dependency or environment mismatch

Symptoms: module not found, incompatible version, unavailable command,
permission denied.

Checks: inspect declared dependencies and documented commands; confirm actual
executable and version; prefer the project's existing environment; avoid global
installs or broad upgrades without authorization.

## Implementation mismatch

Symptoms: test failure, unexpected behavior, edge case regression.

Checks: reduce to the smallest failing input; read the precise assertion or
consumer expectation; compare before/after behavior; avoid unrelated refactors
until the focused failure is explained.

## Validation mismatch

Symptoms: artifact looks plausible but verifier rejects it; a local check passes
but the intended interface fails.

Checks: confirm exact validator, working directory, inputs, filenames, paths,
permissions, encoding, and output channels. Check whether semantic behavior,
not merely syntax, is expected.

## Escalation rule

Ask for clarification instead of guessing when resolution requires a decision
about business semantics, data deletion/transmission/publication, credentials or
authorization, conflicting sources of truth, or a material unspecified trade-off.
