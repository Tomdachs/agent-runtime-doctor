# Agent Runtime Doctor

[![CI](https://github.com/Tomdachs/agent-runtime-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/Tomdachs/agent-runtime-doctor/actions/workflows/ci.yml) [![Release](https://img.shields.io/github/v/release/Tomdachs/agent-runtime-doctor)](https://github.com/Tomdachs/agent-runtime-doctor/releases/latest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**One safe support report for your coding-agent setup.**

Agent Runtime Doctor checks the local runtime health of **Codex, Claude Code, and Gemini CLI**, then turns the results into one small, privacy-minimized report you can paste into a GitHub issue or support ticket.

- **Read-only:** it never repairs permissions, credentials, sandboxes, firewalls, or agent config.
- **Native-first:** provider doctor commands remain the source of truth; this tool normalizes their support-safe summary.
- **Cross-platform:** designed for Windows, WSL, Linux, macOS, containers, and CI.

## Try it now

Python 3.11+ and [uv](https://docs.astral.sh/uv/) are required for the current alpha release.

```bash
uvx --from https://github.com/Tomdachs/agent-runtime-doctor/releases/download/v0.1.0/agent_runtime_doctor-0.1.0-py3-none-any.whl agent-runtime-doctor doctor
```

Typical output:

```text
Agent Runtime Doctor 0.1.0
Overall: OK
Platform: Linux ... (WSL / Ubuntu)

Codex: detected
  native: OK
Claude Code: NOT FOUND
Gemini CLI: NOT FOUND
```

## Install from the release

To install the tagged v0.1.0 wheel from GitHub Releases:

```bash
uv tool install https://github.com/Tomdachs/agent-runtime-doctor/releases/download/v0.1.0/agent_runtime_doctor-0.1.0-py3-none-any.whl
agent-runtime-doctor doctor
```

To create a Markdown report for an issue:

```bash
agent-runtime-doctor report --format markdown > agent-runtime-report.md
```

Machine-readable JSON is also available:

```bash
agent-runtime-doctor doctor --json > agent-runtime-report.json
```

## When it helps

Use Agent Runtime Doctor when:

- an agent works on one machine but not another;
- Windows/WSL/Linux/macOS behavior differs;
- you need a reproducible support report without pasting raw config or secrets;
- you maintain an agent integration and need a stable, versioned diagnostic schema.

## Current support

| Runtime | Detection | Native diagnostics | Normalized report |
| --- | --- | --- | --- |
| Codex | Yes | `codex doctor --json` | Yes |
| Claude Code | Yes | Planned where safe/stable | Version signal |
| Gemini CLI | Yes | Planned where safe/stable | Version signal |

## Privacy by default

Public reports omit absolute executable/home paths, environment values, tokens, authentication payloads, raw native-doctor details, repository remotes, and private workspace names. Native output is treated as untrusted input and only an allowlisted summary enters the public schema.

See [docs/privacy.md](docs/privacy.md) and [docs/report-schema.md](docs/report-schema.md).

## What this project is not

Agent Runtime Doctor is not an auto-repair tool, agent launcher, policy control plane, or replacement for provider support tooling. Its job is to produce small, comparable, shareable diagnostic evidence.

See [docs/architecture.md](docs/architecture.md), [docs/competitive-landscape.md](docs/competitive-landscape.md), and [ROADMAP.md](ROADMAP.md).

## Development

```bash
uv sync --frozen
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

CI validates Linux, Windows, macOS, and package installation. Issues and pull requests are welcome; please read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before sharing diagnostic output.

## License

MIT
