from pathlib import Path

from agent_runtime_doctor.redaction import redact_text


def test_redacts_common_secret_shapes_and_home_path() -> None:
    value = (
        f"home={Path.home()}/private-project/config.toml "
        "token=super-secret-value "
        "Bearer abcdefghijklmnop "
        "ghp_1234567890abcdefghijkl "
        "person@example.com "
        "https://user:pass@example.com/repo"
    )
    redacted = redact_text(value)
    assert str(Path.home()) not in redacted
    assert "private-project" not in redacted
    assert "super-secret-value" not in redacted
    assert "abcdefghijklmnop" not in redacted
    assert "ghp_" not in redacted
    assert "person@example.com" not in redacted
    assert "user:pass@" not in redacted
    assert "<user-path>" in redacted
    assert "<redacted>" in redacted


def test_redaction_flattens_control_characters_and_limits_output() -> None:
    redacted = redact_text("hello\nworld\x00" + "x" * 100, limit=20)
    assert "\n" not in redacted
    assert "\x00" not in redacted
    assert len(redacted) == 20
    assert redacted.endswith("…")


def test_redacts_cross_platform_user_paths_and_private_ip_addresses() -> None:
    value = (
        "/home/alice/private/repo "
        "/Users/bob/work/repo "
        "/mnt/c/Users/Carol/repo "
        r"C:\Users\Dave\repo "
        "192.168.1.25"
    )
    redacted = redact_text(value)
    for private in ("alice", "bob", "Carol", "Dave", "repo", "192.168.1.25"):
        assert private not in redacted
    assert redacted.count("<user-path>") == 4
    assert "<private-ip>" in redacted


def test_dotted_public_version_like_value_is_not_treated_as_private_ip() -> None:
    assert "6.18.33.2" in redact_text("kernel 6.18.33.2")
