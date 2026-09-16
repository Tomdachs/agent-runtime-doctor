from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

DiagnosticStatus = Literal[
    "ok",
    "warning",
    "fail",
    "unavailable",
    "unsupported",
    "error",
]
OverallStatus = Literal["ok", "warning", "fail"]


@dataclass(frozen=True, slots=True)
class PlatformInfo:
    system: str
    release: str
    machine: str
    wsl: bool
    wsl_distribution: str | None = None


@dataclass(frozen=True, slots=True)
class NativeIssue:
    id: str
    category: str
    status: Literal["warning", "fail"]
    summary: str


@dataclass(frozen=True, slots=True)
class NativeDiagnostics:
    source: str
    status: DiagnosticStatus
    schema_version: int | None = None
    counts: dict[str, int] = field(default_factory=dict)
    issues: tuple[NativeIssue, ...] = ()
    note: str | None = None


@dataclass(frozen=True, slots=True)
class AgentResult:
    id: str
    display_name: str
    installed: bool
    version: str | None
    native_diagnostics: NativeDiagnostics


@dataclass(frozen=True, slots=True)
class DoctorReport:
    schema_version: int
    generated_at: str
    tool_version: str
    overall_status: OverallStatus
    platform: PlatformInfo
    agents: tuple[AgentResult, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
