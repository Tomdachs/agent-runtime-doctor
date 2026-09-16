from __future__ import annotations

import subprocess
import threading
from dataclasses import dataclass
from typing import BinaryIO

DEFAULT_MAX_OUTPUT_BYTES = 1_048_576


@dataclass(frozen=True, slots=True)
class ProcessResult:
    returncode: int | None
    stdout: str
    stderr: str
    timed_out: bool
    output_truncated: bool


def _bounded_reader(stream: BinaryIO, limit: int, bucket: dict[str, object], key: str) -> None:
    chunks: list[bytes] = []
    stored = 0
    total_seen = 0
    while True:
        chunk = stream.read(65_536)
        if not chunk:
            break
        total_seen += len(chunk)
        if stored < limit:
            keep = chunk[: limit - stored]
            chunks.append(keep)
            stored += len(keep)
    truncated = total_seen > limit
    bucket[key] = b"".join(chunks)
    bucket[f"{key}_truncated"] = truncated


def run_process(
    executable: str,
    args: list[str],
    *,
    timeout: float,
    max_output_bytes: int = DEFAULT_MAX_OUTPUT_BYTES,
) -> ProcessResult:
    process = subprocess.Popen(  # noqa: S603 - executable is resolved by a runtime adapter
        [executable, *args],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    )
    assert process.stdout is not None
    assert process.stderr is not None

    bucket: dict[str, object] = {}
    stdout_thread = threading.Thread(
        target=_bounded_reader,
        args=(process.stdout, max_output_bytes, bucket, "stdout"),
        daemon=True,
    )
    stderr_thread = threading.Thread(
        target=_bounded_reader,
        args=(process.stderr, max_output_bytes, bucket, "stderr"),
        daemon=True,
    )
    stdout_thread.start()
    stderr_thread.start()

    timed_out = False
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        process.wait()

    stdout_thread.join()
    stderr_thread.join()
    stdout = bytes(bucket.get("stdout", b"")).decode("utf-8", errors="replace")
    stderr = bytes(bucket.get("stderr", b"")).decode("utf-8", errors="replace")
    truncated = bool(bucket.get("stdout_truncated")) or bool(bucket.get("stderr_truncated"))
    return ProcessResult(process.returncode, stdout, stderr, timed_out, truncated)
