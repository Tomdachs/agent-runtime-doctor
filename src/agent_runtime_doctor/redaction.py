from __future__ import annotations

import ipaddress
import re
from pathlib import Path

_EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
_BEARER = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{8,}")
_KNOWN_TOKEN = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9_]{12,}|github_pat_[A-Za-z0-9_]{12,})\b"
)
_SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(api[_-]?key|token|secret|password|passwd)\s*([:=])\s*([^\s,;]+)"
)
_URL_CREDENTIALS = re.compile(r"(?i)(https?://)([^/@\s]+):([^/@\s]+)@")
_USER_PATHS = (
    re.compile(r"(?i)/home/[^/\s]+(?:/[^\s,;]+)*"),
    re.compile(r"(?i)/Users/[^/\s]+(?:/[^\s,;]+)*"),
    re.compile(r"(?i)/mnt/[a-z]/Users/[^/\s]+(?:/[^\s,;]+)*"),
    re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s]+(?:\\[^\s,;]+)*"),
)
_IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def _redact_private_ip(match: re.Match[str]) -> str:
    try:
        address = ipaddress.ip_address(match.group(0))
    except ValueError:
        return match.group(0)
    return "<private-ip>" if address.is_private else match.group(0)


def redact_text(value: str, *, limit: int = 300) -> str:
    """Return a single-line, support-safe representation of untrusted command output."""
    text = _CONTROL.sub("", value).replace("\r", " ").replace("\n", " ").strip()

    # Replace the current home first, including descendants, so private workspace names are omitted.
    home = str(Path.home())
    if home:
        home_pattern = re.compile(rf"{re.escape(home)}(?:[/\\][^\s,;]+)*")
        text = home_pattern.sub("<user-path>", text)
    for pattern in _USER_PATHS:
        text = pattern.sub("<user-path>", text)

    text = _EMAIL.sub("<email>", text)
    text = _BEARER.sub("Bearer <redacted>", text)
    text = _KNOWN_TOKEN.sub("<redacted-token>", text)
    text = _SECRET_ASSIGNMENT.sub(r"\1\2<redacted>", text)
    text = _URL_CREDENTIALS.sub(r"\1<credentials>@", text)
    text = _IPV4.sub(_redact_private_ip, text)
    if len(text) > limit:
        return text[: limit - 1] + "…"
    return text
