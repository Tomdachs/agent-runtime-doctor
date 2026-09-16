from __future__ import annotations

import json
from collections import Counter

from agent_runtime_doctor.adapters.common import read_version, resolve_executable
from agent_runtime_doctor.models import AgentResult, NativeDiagnostics, NativeIssue
from agent_runtime_doctor.redaction import redact_text
from agent_runtime_doctor.runner import run_process

_ALLOWED_NATIVE_STATUSES = {"ok", "warning", "fail"}


def _parse_native_report(payload: str) -> NativeDiagnostics:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return NativeDiagnostics(
            source="codex doctor --json",
            status="error",
            note="native doctor returned invalid JSON",
        )
    if not isinstance(data, dict) or not isinstance(data.get("checks"), dict):
        return NativeDiagnostics(
            source="codex doctor --json",
            status="error",
            note="native doctor returned an unsupported JSON shape",
        )

    raw_overall = data.get("overallStatus")
    if raw_overall not in _ALLOWED_NATIVE_STATUSES:
        return NativeDiagnostics(
            source="codex doctor --json",
            status="error",
            note="native doctor returned an unknown overall status",
        )

    counts: Counter[str] = Counter()
    issues: list[NativeIssue] = []
    for check_key, raw_check in data["checks"].items():
        if not isinstance(check_key, str) or not isinstance(raw_check, dict):
            continue
        status = raw_check.get("status")
        if status not in _ALLOWED_NATIVE_STATUSES:
            counts["unknown"] += 1
            continue
        counts[status] += 1
        if status not in {"warning", "fail"}:
            continue
        check_id = raw_check.get("id")
        category = raw_check.get("category")
        summary = raw_check.get("summary")
        issues.append(
            NativeIssue(
                id=redact_text(check_id if isinstance(check_id, str) else check_key, limit=120),
                category=redact_text(
                    category if isinstance(category, str) else "unknown", limit=80
                ),
                status=status,
                summary=redact_text(summary if isinstance(summary, str) else "non-ok native check"),
            )
        )

    schema_version = data.get("schemaVersion")
    if not isinstance(schema_version, int):
        schema_version = None
    return NativeDiagnostics(
        source="codex doctor --json",
        status=raw_overall,
        schema_version=schema_version,
        counts=dict(sorted(counts.items())),
        issues=tuple(issues),
    )


def parse_codex_doctor_json(payload: str) -> NativeDiagnostics:
    """Parse only the public, support-safe subset of Codex doctor JSON."""
    return _parse_native_report(payload)


class CodexAdapter:
    id = "codex"
    display_name = "Codex"

    def diagnose(self, *, run_native: bool, timeout: float) -> AgentResult:
        executable = resolve_executable("codex")
        if executable is None:
            return AgentResult(
                id=self.id,
                display_name=self.display_name,
                installed=False,
                version=None,
                native_diagnostics=NativeDiagnostics(
                    source="none", status="unavailable", note="runtime not found on PATH"
                ),
            )

        version = read_version(executable, ["--version"], timeout=timeout)
        if not run_native:
            native = NativeDiagnostics(
                source="codex doctor --json",
                status="unsupported",
                note="native diagnostics skipped by request",
            )
            return AgentResult(self.id, self.display_name, True, version, native)

        result = run_process(
            executable,
            ["doctor", "--json"],
            timeout=timeout,
            max_output_bytes=1_048_576,
        )
        if result.timed_out:
            native = NativeDiagnostics(
                source="codex doctor --json", status="error", note="native doctor timed out"
            )
        elif result.output_truncated:
            native = NativeDiagnostics(
                source="codex doctor --json",
                status="error",
                note="native doctor exceeded the output limit",
            )
        elif not result.stdout.strip():
            native = NativeDiagnostics(
                source="codex doctor --json",
                status="error",
                note="native doctor returned no JSON output",
            )
        else:
            native = _parse_native_report(result.stdout)
            if result.returncode not in {0, 1} and native.status != "fail":
                native = NativeDiagnostics(
                    source="codex doctor --json",
                    status="error",
                    note="native doctor exited unexpectedly",
                )
        return AgentResult(self.id, self.display_name, True, version, native)
