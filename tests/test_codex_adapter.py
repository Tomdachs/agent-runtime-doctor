import json
from pathlib import Path

from agent_runtime_doctor.adapters.codex import parse_codex_doctor_json


def test_codex_parser_keeps_only_allowlisted_support_summary() -> None:
    secret = "Bearer abcdefghijklmnop"
    payload = json.dumps(
        {
            "schemaVersion": 1,
            "generatedAt": "ignored",
            "overallStatus": "warning",
            "codexVersion": "ignored",
            "checks": {
                "sandbox.runtime": {
                    "id": "sandbox.runtime",
                    "category": "sandbox",
                    "status": "warning",
                    "summary": f"config at {Path.home()}/private; token=top-secret",
                    "details": {"authorization": secret, "repo": "private-name"},
                    "remediation": f"run something with {secret}",
                    "durationMs": 12,
                },
                "network": {
                    "id": "network",
                    "category": "network",
                    "status": "ok",
                    "summary": "connected",
                    "details": {"proxy": "https://user:pass@example.com"},
                    "durationMs": 3,
                },
            },
        }
    )
    result = parse_codex_doctor_json(payload)
    assert result.status == "warning"
    assert result.schema_version == 1
    assert result.counts == {"ok": 1, "warning": 1}
    assert len(result.issues) == 1
    issue = result.issues[0]
    assert issue.id == "sandbox.runtime"
    assert issue.category == "sandbox"
    assert str(Path.home()) not in issue.summary
    assert "top-secret" not in issue.summary
    serialized = repr(result)
    assert secret not in serialized
    assert "private-name" not in serialized


def test_codex_parser_rejects_malformed_or_unknown_schema_shape() -> None:
    invalid = parse_codex_doctor_json("not-json")
    assert invalid.status == "error"

    wrong_shape = parse_codex_doctor_json(json.dumps({"overallStatus": "ok", "checks": []}))
    assert wrong_shape.status == "error"


def test_codex_parser_rejects_unknown_overall_status() -> None:
    result = parse_codex_doctor_json(json.dumps({"overallStatus": "mystery", "checks": {}}))
    assert result.status == "error"
