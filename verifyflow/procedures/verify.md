# Verification Procedure

## Goal

Demonstrate that the requested result is present and correct through direct,
task-relevant evidence.

## Derive checks from the contract

Use only checks tied to actual requirements. Examples:

- Artifact exists at the required path
- Required files, fields, sections, or outputs are present
- File parses according to its stated format
- Output conforms to a known schema or interface
- Focused tests pass
- A command returns the expected output and exit status
- Intended behavior is observed through its consumer-facing interface
- No unintended change occurred within the affected scope

Do not substitute a plausible-looking artifact for a checked one.

## Prefer independent verification

When practical, choose a check different from construction:

- Parse generated JSON instead of only reading it
- Run a focused test instead of only inspecting source
- Open output with a compatible consumer or validator
- Compare required fields against an explicit schema
- Inspect a diff after a transformation

A check is useful only if it could detect a meaningful failure.

## Validate final artifacts

For simple structural checks, run:

```bash
python scripts/validate_artifact.py --path <artifact> --type auto
```

Add only task-derived checks, for example:

```bash
python scripts/validate_artifact.py \
  --path output/report.json --type json \
  --required summary --required results
```

This helper is intentionally read-only and limited. It does not prove semantic
correctness, execute artifacts, access a network, or replace task-specific tests.

## Check boundaries

Before completion, confirm the correct target was modified or produced, the
result is in the required location, relevant checks passed, and no known failure
or unverified assumption is concealed. Confirm no external or irreversible
operation exceeded the authorized scope.

## Report accurately

Report: (1) what was delivered or changed, (2) checks actually run and their
observed results, and (3) any material limitation or unverified condition. Do
not say “verified,” “fixed,” “complete,” or “works” when only an edit occurred.
