import json
from pathlib import Path

import jsonschema

from agent_runtime_doctor.doctor import collect_report
from agent_runtime_doctor.models import AgentResult, NativeDiagnostics
from agent_runtime_doctor.render import render_json, render_markdown


class FakeAdapter:
    def __init__(self, result: AgentResult) -> None:
        self.result = result

    def diagnose(self, *, run_native: bool, timeout: float) -> AgentResult:
        assert isinstance(run_native, bool)
        assert timeout > 0
        return self.result


def test_report_matches_checked_in_json_schema() -> None:
    result = AgentResult(
        id="example",
        display_name="Example Agent",
        installed=True,
        version="1.2.3",
        native_diagnostics=NativeDiagnostics(source="example doctor --json", status="ok"),
    )
    report = collect_report(adapters=(FakeAdapter(result),), timeout=1)
    payload = json.loads(render_json(report))
    schema = json.loads(Path("schema/report-v1.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(payload)
    assert report.overall_status == "ok"


def test_native_error_degrades_overall_to_warning() -> None:
    result = AgentResult(
        id="example",
        display_name="Example Agent",
        installed=True,
        version=None,
        native_diagnostics=NativeDiagnostics(source="doctor", status="error"),
    )
    report = collect_report(adapters=(FakeAdapter(result),), timeout=1)
    assert report.overall_status == "warning"


def test_no_installed_runtime_is_warning() -> None:
    result = AgentResult(
        id="example",
        display_name="Example Agent",
        installed=False,
        version=None,
        native_diagnostics=NativeDiagnostics(source="none", status="unavailable"),
    )
    report = collect_report(adapters=(FakeAdapter(result),), timeout=1)
    assert report.overall_status == "warning"


def test_markdown_contains_privacy_notice() -> None:
    result = AgentResult(
        id="example",
        display_name="Example Agent",
        installed=True,
        version="1.0",
        native_diagnostics=NativeDiagnostics(source="none", status="unsupported"),
    )
    report = collect_report(adapters=(FakeAdapter(result),), timeout=1)
    output = render_markdown(report)
    assert "Privacy:" in output
    assert "Example Agent" in output
