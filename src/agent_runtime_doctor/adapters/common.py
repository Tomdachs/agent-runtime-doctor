from __future__ import annotations

import shutil

from agent_runtime_doctor.redaction import redact_text
from agent_runtime_doctor.runner import run_process


def resolve_executable(name: str) -> str | None:
    return shutil.which(name)


def read_version(executable: str, args: list[str], *, timeout: float) -> str | None:
    result = run_process(executable, args, timeout=min(timeout, 10.0), max_output_bytes=32_768)
    if result.timed_out or result.output_truncated:
        return None
    output = result.stdout.strip() or result.stderr.strip()
    if not output:
        return None
    first_line = next((line.strip() for line in output.splitlines() if line.strip()), "")
    return redact_text(first_line, limit=200) or None
