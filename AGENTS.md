# AGENTS.md

## Scope

This repository is a public, local-first diagnostic CLI for coding-agent runtimes.
Keep repository-specific guidance here; user workflows belong in README/docs and executable defaults belong in code.

## Product boundaries

- Prefer each agent's native diagnostic command over reimplementing provider-specific health logic.
- Keep default operation read-only. Never auto-repair permissions, credentials, sandboxes, firewalls, or agent configuration.
- Never print secret values, raw environment variables, authentication payloads, or unredacted native diagnostic details.
- Treat executable paths and native command output as untrusted input. Use resolved executables directly and bounded timeouts.
- A missing optional runtime is an observable state, not an error in Agent Runtime Doctor itself.

## Change requirements

- Behavior/schema changes require tests and documentation updates.
- Preserve the versioned public JSON schema unless a documented schema-version change is intentional.
- Run `uv run ruff check .`, `uv run ruff format --check .`, and `uv run pytest` before committing code changes.
- Keep dependencies minimal and cross-platform; justify new runtime dependencies in the pull request or commit context.
