from __future__ import annotations

import os
import platform
from pathlib import Path

from agent_runtime_doctor.models import PlatformInfo
from agent_runtime_doctor.redaction import redact_text


def _linux_pretty_name() -> str | None:
    path = Path("/etc/os-release")
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    values: dict[str, str] = {}
    for line in lines:
        if "=" not in line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"')
    return values.get("PRETTY_NAME") or values.get("NAME")


def detect_platform() -> PlatformInfo:
    release = platform.release()
    wsl = bool(os.environ.get("WSL_INTEROP") or os.environ.get("WSL_DISTRO_NAME"))
    if not wsl and platform.system() == "Linux":
        wsl = "microsoft" in release.lower()
    distro = os.environ.get("WSL_DISTRO_NAME") if wsl else None
    if wsl and not distro:
        distro = _linux_pretty_name()
    return PlatformInfo(
        system=redact_text(platform.system(), limit=80),
        release=redact_text(release, limit=120),
        machine=redact_text(platform.machine(), limit=80),
        wsl=wsl,
        wsl_distribution=redact_text(distro, limit=120) if distro else None,
    )
