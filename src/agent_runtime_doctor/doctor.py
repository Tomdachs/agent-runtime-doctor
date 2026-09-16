from __future__ import annotations

from datetime import UTC, datetime

from agent_runtime_doctor import __version__
from agent_runtime_doctor.adapters import ClaudeCodeAdapter, CodexAdapter, GeminiCliAdapter
from agent_runtime_doctor.adapters.base import RuntimeAdapter
from agent_runtime_doctor.models import AgentResult, DoctorReport, OverallStatus
from agent_runtime_doctor.platform_info import detect_platform

_DEFAULT_ADAPTERS: tuple[RuntimeAdapter, ...] = (
    CodexAdapter(),
    ClaudeCodeAdapter(),
    GeminiCliAdapter(),
)


def _overall_status(agents: tuple[AgentResult, ...]) -> OverallStatus:
    installed = [agent for agent in agents if agent.installed]
    if not installed:
        return "warning"
    statuses = {agent.native_diagnostics.status for agent in installed}
    if "fail" in statuses:
        return "fail"
    if "warning" in statuses or "error" in statuses:
        return "warning"
    return "ok"


def collect_report(
    *,
    run_native: bool = True,
    timeout: float = 45.0,
    adapters: tuple[RuntimeAdapter, ...] = _DEFAULT_ADAPTERS,
) -> DoctorReport:
    agents = tuple(adapter.diagnose(run_native=run_native, timeout=timeout) for adapter in adapters)
    return DoctorReport(
        schema_version=1,
        generated_at=datetime.now(UTC).isoformat(timespec="seconds"),
        tool_version=__version__,
        overall_status=_overall_status(agents),
        platform=detect_platform(),
        agents=agents,
    )
