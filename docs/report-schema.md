# Report schema

The public interchange contract is [`schema/report-v1.json`](../schema/report-v1.json).

## Status semantics

`overall_status` describes the diagnostic run, not a guarantee that every installed agent is healthy.

- `ok`: no supported native diagnostic reported warning/failure and no adapter errored.
- `warning`: no installed supported runtime was found, or an installed adapter/native diagnostic could not be completed cleanly.
- `fail`: at least one authoritative native diagnostic reported `fail`.

Per-runtime native status is more specific:

- `ok`, `warning`, `fail`: passed through from a supported structured native doctor.
- `unavailable`: runtime executable was not found.
- `unsupported`: runtime is present but this version of Agent Runtime Doctor has no structured native-doctor adapter, or native execution was explicitly skipped.
- `error`: the native command timed out, exceeded the output limit, or returned unsupported/malformed structured data.

## Compatibility

Schema version `1` is intentionally small. Additive fields may be introduced only when existing consumers that ignore unknown fields remain correct. Because the checked-in JSON Schema currently disallows additional properties, any additive contract change must update this file and its tests in the same commit.

Breaking changes require a new schema file/version rather than silently changing v1 semantics.
