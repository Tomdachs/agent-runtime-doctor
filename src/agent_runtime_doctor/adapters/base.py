from __future__ import annotations

from typing import Protocol

from agent_runtime_doctor.models import AgentResult


class RuntimeAdapter(Protocol):
    def diagnose(self, *, run_native: bool, timeout: float) -> AgentResult: ...
