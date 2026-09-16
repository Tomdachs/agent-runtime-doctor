# Contributing

Thanks for helping improve Agent Runtime Doctor.

## Before opening an issue

Run the latest release when possible and include the privacy-minimized Markdown or JSON report. Review it before posting. Do not paste tokens, API keys, cookies, private repository URLs, or unredacted output from an underlying agent command.

## Development

Requirements: Git, Python 3.11+, and `uv`.

```bash
uv sync --frozen
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Keep provider-specific behavior in an adapter. Prefer a provider's native structured diagnostics to local reimplementation.

## Pull requests

- Add tests for behavior or schema changes.
- Keep default behavior read-only.
- Avoid new runtime dependencies unless they materially simplify safe cross-platform behavior.
- Update docs when public commands, fields, privacy behavior, or support boundaries change.
- Keep commits focused enough to review independently.

## Issues for new runtimes

A useful adapter request links the runtime's official diagnostic/install documentation and describes what stable machine-readable signal is available. Interactive-only probes should not be made a default unattended check.
