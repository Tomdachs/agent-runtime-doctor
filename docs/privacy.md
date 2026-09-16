# Privacy and redaction

Diagnostic tools can accidentally turn local troubleshooting into credential disclosure. Agent Runtime Doctor therefore treats public-report safety as a product requirement, not a renderer option.

## Never collected into the normalized report

- token/API-key/cookie values;
- raw environment-variable values;
- raw authentication responses;
- repository remotes;
- arbitrary file contents;
- raw provider-native diagnostic details.

## Minimized fields

Executable discovery records only whether a supported runtime was found. The public report does not include its absolute path. Platform data uses broad OS/release/architecture fields; WSL distribution name is included because it materially changes runtime behavior.

## Native diagnostic handling

Provider output is parsed in memory. The adapter allowlists identifiers, statuses, high-level summaries, schema version, and aggregate counts needed for support. Unknown fields are ignored.

A malformed or unexpectedly large native response becomes a diagnostic failure for that adapter; it is not copied verbatim into the report.

## Sharing reports

The default JSON and Markdown formats are intended to be safer to paste into a public issue, but users should still review any diagnostic report before publishing it. Security-sensitive reports should be shared through the affected project's private security channel when appropriate.
