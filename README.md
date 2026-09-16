# Agent Runtime Doctor

[![CI](https://github.com/Tomdachs/agent-runtime-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/Tomdachs/agent-runtime-doctor/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Agent Runtime Doctor is a local-first CLI that turns coding-agent health signals into one privacy-minimized support report.

It is intentionally **native-first**: when an agent already ships a doctor command, Agent Runtime Doctor calls that command instead of duplicating its provider-specific logic, then normalizes only the support-safe summary. The first implementation target is Codex, with adapters for additional coding agents following the same boundary.

## Why another doctor?

Codex now ships a strong `codex doctor --json`, and Claude Code also has native installation diagnostics. Those tools are the source of truth for their own runtimes. Agent Runtime Doctor targets a different problem: developers increasingly use several coding agents across Windows, WSL, Linux, macOS, containers, and CI, but support reports are fragmented and often contain more local detail than an issue needs.

This project provides:

- one stable, versioned report schema across supported agents;
- native diagnostic orchestration rather than replacement;
- privacy-minimized output suitable for a public issue by default;
- explicit distinction between `ok`, `warning`, `fail`, `unavailable`, `unsupported`, and `error`;
- bounded, read-only probes with no automatic permission or configuration repair;
- a base for future CI and cross-agent environment compatibility checks.

## Status

Early MVP. The repository is public from the start so design decisions, issues, and maintenance history remain auditable.

Current scope:

- platform/WSL detection;
- Codex discovery, version detection, and normalized `codex doctor --json` summary;
- Claude Code and Gemini CLI discovery/version signals;
- human, JSON, and Markdown support output;
- redaction tests and schema contract tests.

## Quick start

Python 3.11+ is required during the alpha phase.

```bash
# From a checkout
uv sync --frozen
uv run agent-runtime-doctor doctor

# Machine-readable support report
uv run agent-runtime-doctor doctor --json

# Markdown suitable for a GitHub issue
uv run agent-runtime-doctor report --format markdown
```

The CLI does not change agent configuration, credentials, ACLs, sandbox policy, firewall rules, or operating-system settings.

## Privacy model

Default reports intentionally omit:

- absolute executable and home-directory paths;
- environment-variable values;
- tokens, API keys, cookies, and authentication payloads;
- raw native-doctor detail fields;
- repository remotes and private workspace names.

Native doctor output is treated as untrusted input. Only an allowlisted summary is normalized into the public schema. See [docs/privacy.md](docs/privacy.md).

## Project boundary

Agent Runtime Doctor is **not** an auto-repair tool, agent launcher, policy control plane, or replacement for provider support tooling. See [docs/architecture.md](docs/architecture.md), [docs/competitive-landscape.md](docs/competitive-landscape.md), and [ROADMAP.md](ROADMAP.md).

## Development

```bash
uv sync --frozen
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

CI runs the same checks on Linux, Windows, and macOS across supported Python versions.

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before sharing diagnostic output.

## License

MIT
