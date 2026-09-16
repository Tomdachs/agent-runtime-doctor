from agent_runtime_doctor.cli import main


def test_empty_invocation_is_success() -> None:
    assert main([]) == 0
