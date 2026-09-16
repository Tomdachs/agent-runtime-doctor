from __future__ import annotations

import json

from agent_runtime_doctor.models import AgentResult, DoctorReport, NativeDiagnostics

_STATUS_LABEL = {
    "ok": "OK",
    "warning": "WARN",
    "fail": "FAIL",
    "unavailable": "NOT FOUND",
    "unsupported": "NOT CHECKED",
    "error": "ERROR",
}


def render_json(report: DoctorReport) -> str:
    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2, sort_keys=True)


def _native_summary(native: NativeDiagnostics) -> str:
    label = _STATUS_LABEL[native.status]
    if native.counts:
        counts = ", ".join(f"{key}={value}" for key, value in native.counts.items())
        return f"{label} ({counts})"
    if native.note:
        return f"{label} ({native.note})"
    return label


def _agent_lines(agent: AgentResult) -> list[str]:
    if not agent.installed:
        return [f"{agent.display_name}: NOT FOUND"]
    version = f" ({agent.version})" if agent.version else ""
    lines = [
        f"{agent.display_name}: detected{version}",
        f"  native: {_native_summary(agent.native_diagnostics)}",
    ]
    for issue in agent.native_diagnostics.issues:
        lines.append(f"  - {issue.status.upper()} {issue.id}: {issue.summary}")
    return lines


def render_human(report: DoctorReport) -> str:
    platform = f"{report.platform.system} {report.platform.release} {report.platform.machine}"
    if report.platform.wsl:
        suffix = (
            f" / {report.platform.wsl_distribution}" if report.platform.wsl_distribution else ""
        )
        platform += f" (WSL{suffix})"
    lines = [
        f"Agent Runtime Doctor {report.tool_version}",
        f"Overall: {_STATUS_LABEL[report.overall_status]}",
        f"Platform: {platform}",
        "",
    ]
    for index, agent in enumerate(report.agents):
        if index:
            lines.append("")
        lines.extend(_agent_lines(agent))
    return "\n".join(lines)


def render_markdown(report: DoctorReport) -> str:
    platform = f"{report.platform.system} {report.platform.release} ({report.platform.machine})"
    if report.platform.wsl:
        distro = (
            f" / {report.platform.wsl_distribution}" if report.platform.wsl_distribution else ""
        )
        platform += f" / WSL{distro}"
    lines = [
        "## Agent Runtime Doctor report",
        "",
        f"- Tool: `{report.tool_version}`",
        f"- Schema: `{report.schema_version}`",
        f"- Overall: **{_STATUS_LABEL[report.overall_status]}**",
        f"- Platform: `{platform}`",
        "",
        "| Runtime | Version | Native diagnostics |",
        "| --- | --- | --- |",
    ]
    for agent in report.agents:
        version = agent.version or ("not found" if not agent.installed else "unknown")
        native = _native_summary(agent.native_diagnostics)
        lines.append(f"| {agent.display_name} | `{version}` | {native} |")
    issues = [
        (agent.display_name, issue)
        for agent in report.agents
        for issue in agent.native_diagnostics.issues
    ]
    if issues:
        lines.extend(["", "### Non-OK native checks", ""])
        for display_name, issue in issues:
            lines.append(f"- **{display_name} / {issue.id}** ({issue.status}): {issue.summary}")
    lines.extend(
        [
            "",
            "> Privacy: this normalized report omits raw native details, environment values, "
            "and executable paths. Review it before publishing.",
        ]
    )
    return "\n".join(lines)
