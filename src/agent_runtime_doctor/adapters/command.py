from __future__ import annotations

from dataclasses import dataclass

from agent_runtime_doctor.adapters.common import read_version, resolve_executable
from agent_runtime_doctor.models import AgentResult, NativeDiagnostics


@dataclass(frozen=True, slots=True)
class VersionOnlyAdapter:
    id: str
    display_name: str
    executable_name: str
    version_args: tuple[str, ...] = ("--version",)

    def diagnose(self, *, run_native: bool, timeout: float) -> AgentResult:
        del run_native
        executable = resolve_executable(self.executable_name)
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
        version = read_version(executable, list(self.version_args), timeout=timeout)
        return AgentResult(
            id=self.id,
            display_name=self.display_name,
            installed=True,
            version=version,
            native_diagnostics=NativeDiagnostics(
                source="none",
                status="unsupported",
                note="no structured native diagnostic adapter yet",
            ),
        )


class ClaudeCodeAdapter(VersionOnlyAdapter):
    def __init__(self) -> None:
        super().__init__("claude-code", "Claude Code", "claude")


class GeminiCliAdapter(VersionOnlyAdapter):
    def __init__(self) -> None:
        super().__init__("gemini-cli", "Gemini CLI", "gemini")
