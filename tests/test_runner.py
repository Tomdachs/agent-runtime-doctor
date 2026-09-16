import sys

from agent_runtime_doctor.runner import run_process


def test_runner_caps_captured_output() -> None:
    result = run_process(
        sys.executable,
        ["-c", "import sys; sys.stdout.write('x' * 101)"],
        timeout=5,
        max_output_bytes=100,
    )
    assert result.returncode == 0
    assert len(result.stdout.encode()) == 100
    assert result.output_truncated is True


def test_runner_does_not_mark_exact_limit_as_truncated() -> None:
    result = run_process(
        sys.executable,
        ["-c", "import sys; sys.stdout.write('x' * 100)"],
        timeout=5,
        max_output_bytes=100,
    )
    assert result.returncode == 0
    assert result.output_truncated is False


def test_runner_enforces_timeout() -> None:
    result = run_process(
        sys.executable,
        ["-c", "import time; time.sleep(2)"],
        timeout=0.1,
    )
    assert result.timed_out is True
    assert result.returncode is not None
