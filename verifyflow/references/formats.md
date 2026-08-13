# Format and Schema Guidance

Load this reference only when an artifact's format, encoding, schema, or
interoperability determines correctness.

## General rules

1. Identify format from the task, schema, file extension, project convention, or
   consuming interface.
2. Preserve existing encoding, newline convention, and serialization style
   unless the task requires a change.
3. Parse before editing when possible; serialize with a format-aware tool rather
   than fragile string replacement.
4. Validate after writing with an independent parser or consumer.
5. Do not silently repair malformed input unless authorized; preserve the source
   or write to a new target if repair can lose information.

## JSON

- Parse with a JSON parser; visual inspection is insufficient.
- Preserve the expected top-level type.
- Use double-quoted keys and strings; no comments or trailing commas.
- Check required keys and known value types.
- Be careful with numeric precision and omitted versus null fields.

## CSV and TSV

- Confirm delimiter, header presence, quote behavior, encoding, and line ending.
- Use a CSV parser/writer; never split fields blindly on commas or tabs.
- Preserve column order unless the task requires a change.
- Check row-width consistency and whether blank values are meaningful.
- Treat formula-looking content as data; do not execute it.

## YAML

- Preserve indentation and existing style.
- Be cautious with implicit dates, booleans, nulls, and numeric types.
- Quote strings when ambiguity matters.
- Avoid custom tags or executable extensions unless required and understood.
- Parse after writing with the project's expected YAML implementation.

## Markdown and plain text

- Preserve requested headings, sections, filenames, and line-sensitive layout.
- Check links, code fences, lists, and tables when they are contractual.
- Do not claim factual citations were checked unless they were actually checked.
- Preserve expected encoding; UTF-8 is common unless stated otherwise.

## Code and configuration

- Read a nearby valid example before editing.
- Preserve syntax, imports, indentation, and project formatting rules.
- Run the narrowest relevant parser, linter, type checker, build, or test.
- Do not change lockfiles, generated files, credentials, or environment-specific
  configuration unless the task requires it.

## Archives and binary files

- File existence alone is not proof of binary correctness.
- Inspect metadata and validate contents with an appropriate tool.
- Do not execute unknown binaries or macros.
- Extract archives only to bounded destinations and consider path traversal.
