from agent_runtime_doctor import cli
from agent_runtime_doctor.models import (
    AgentResult,
    DoctorReport,
    NativeDiagnostics,
    PlatformInfo,
)


def _report(status: str = "ok") -> DoctorReport:
    return DoctorReport(
        schema_version=1,
        generated_at="2026-09-16T00:00:00+00:00",
        tool_version="0.1.0",
        overall_status=status,  # type: ignore[arg-type]
        platform=PlatformInfo("Linux", "test", "x86_64", False),
        agents=(
            AgentResult(
                "example",
                "Example Agent",
                True,
                "1.0",
                NativeDiagnostics("none", "unsupported"),
            ),
        ),
    )


def test_empty_invocation_prints_help(capsys) -> None:
    assert cli.main([]) == 0
    assert "doctor" in capsys.readouterr().out


def test_doctor_json(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "collect_report", lambda **_: _report())
    assert cli.main(["doctor", "--json"]) == 0
    output = capsys.readouterr().out
    assert '"schema_version": 1' in output
    assert '"Example Agent"' in output


def test_fail_status_returns_two(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "collect_report", lambda **_: _report("fail"))
    assert cli.main(["doctor"]) == 2
    assert "Overall: FAIL" in capsys.readouterr().out
