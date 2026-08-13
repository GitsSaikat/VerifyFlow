# Execution Procedure

## Goal

Make the smallest correct change that satisfies the established contract while
preserving scope control, recoverability, and evidence.

## Select the narrowest method

Prefer, in order:

1. An existing project command, test fixture, template, or documented workflow
2. A focused edit to the relevant source or artifact
3. A small deterministic script for repetitive or fragile work
4. New dependencies, frameworks, or broad redesign only when required

Do not add infrastructure merely to make the solution appear general.

## Work in checkpoints

For each material step:

1. State the intended local effect.
2. Apply the smallest scoped action.
3. Inspect command output, diff, generated output, or changed state.
4. Compare observations with the expected local effect.
5. Continue only when the evidence is consistent.

Keep discovery, transformation, validation, and final delivery distinct. Do not
hide multiple unobserved changes inside one broad command sequence.

## Preserve conventions

Match existing naming, structure, formatting, error handling, dependencies,
and test/build commands. If a task requirement conflicts with an established
convention, satisfy the task requirement and state the material trade-off.

## Control side effects

Before a consequential action, confirm exact target paths and identifiers,
whether it overwrites/deletes/transmits/publishes anything, and whether a diff,
preview, dry run, backup, or copy is available. Use explicit paths and bounded
selectors. Avoid wildcards, unscoped recursion, and destructive defaults.

## Handle failure from evidence

When an action fails:

1. Read the exact error, exit status, and relevant context.
2. Classify it: path, input, permissions, dependency, schema, implementation,
   environment, or acceptance mismatch.
3. Form one hypothesis tied to observed evidence.
4. Run the least invasive check that distinguishes that hypothesis.
5. Apply one targeted correction and rerun the focused validation.

Read `references/troubleshooting.md` only if the failure remains unresolved.

## Stop at the contract

Do not add unrelated refactors, optimization, style-only changes, or
unrequested features. Extra change surface raises risk and weakens verification.
