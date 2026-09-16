# Competitive landscape and product boundary

Reviewed 2026-09-16 before implementation.

## Existing tools

### OpenAI Codex `doctor`

OpenAI Codex now has a built-in `codex doctor --json` that checks installation, configuration, authentication, runtime, sandbox, connectivity, state, and related signals. It emits a redacted machine-readable schema and is the authoritative Codex-specific diagnostic source.

Source: <https://github.com/openai/codex/blob/main/codex-rs/cli/src/doctor.rs>

**Decision:** never duplicate Codex-specific health rules. Consume a minimal allowlisted summary from the native command.

### DebadityaHait/coding-agent-doctor

`coding-agent-doctor` is a cross-provider local health check for Claude Code, Codex CLI, and Cursor. It inspects configuration layers, MCP transports/runners, environment-key presence, and emits redacted JSON/Markdown/SARIF reports.

Source: <https://github.com/DebadityaHait/coding-agent-doctor>

**Decision:** do not duplicate broad config/MCP auditing. Keep Agent Runtime Doctor narrower: delegate provider-specific health checks to native doctor commands when available and focus on a minimal cross-provider interchange report that omits raw config evidence by default.

### EXboys/agent-doctor

`agent-doctor` diagnoses and repairs several local agent runtimes, including Claude Code and Codex, with backup/repair flows and an optional team control plane.

Source: <https://github.com/EXboys/agent-doctor>

**Decision:** do not compete on repair, team policy, config synchronization, or desktop management. Agent Runtime Doctor remains read-only and specializes in normalized support evidence and public-report privacy.

### Codex-specific community doctors

Several community projects add Codex health checks, configuration cleanup, or session diagnostics.

Examples:

- <https://github.com/warren2008-2020-spec/codex-doctor>
- <https://github.com/Lumidew/codex-doctor>
- <https://github.com/hj01857655/codex-doctor>

**Decision:** the project name and scope stay provider-neutral, and provider-specific logic remains delegated to native tooling where available.

## Differentiation

The intended niche is a **support interchange layer**:

- cross-agent and cross-platform;
- stable normalized schema;
- read-only orchestration;
- privacy-minimized by default for public issue reports;
- provider-native diagnostics remain authoritative;
- suitable for CI/automation without requiring an agent to reason about the machine.

If an upstream provider exposes a better structured diagnostic, the adapter should become thinner, not more complex.
