# Architecture

## Goal

Produce a small, stable, privacy-minimized diagnostic report across coding-agent runtimes without competing with each provider's native diagnostics.

## Native-first pipeline

```text
resolved executable
      |
      v
version probe --------------------------+
      |                                  |
      v                                  |
provider-native doctor (when supported) |
      |                                  |
      v                                  |
strict parser / allowlist                |
      |                                  |
      +-------------> normalized adapter result
                                      |
platform facts -------------------------+
                                      |
                                      v
                           versioned public report
                           | human | JSON | Markdown |
```

The provider-native result is the source of truth for provider-specific health. Agent Runtime Doctor does not infer that a provider is healthy merely because its binary exists.

## Trust boundaries

1. `PATH` and resolved executable locations are untrusted local input.
2. Native commands run via the resolved executable, never through `shell=True`.
3. Every subprocess has a bounded timeout and output-size cap.
4. Native JSON is parsed defensively and only allowlisted fields cross into the normalized report.
5. Report renderers never receive secrets or raw environment values.
6. Default commands are read-only. Mutation belongs outside this project boundary.

## Adapter contract

Each adapter is responsible for:

- runtime identity and display name;
- executable discovery;
- a bounded version probe;
- optional native-doctor capability detection;
- conversion from native results to the common status vocabulary.

The core owns platform facts, process execution, redaction, schema serialization, and rendering.

## Schema stability

`schema_version` starts at `1`. Additive fields may be introduced without incrementing the version when old consumers remain valid. Breaking field meaning, type, or requiredness requires a schema-version change plus migration notes.

## Deferred work

- standalone release binaries;
- GitHub Action wrapper;
- additional provider-native doctor parsers;
- container/devcontainer checks;
- opt-in detailed local report distinct from public support output.
