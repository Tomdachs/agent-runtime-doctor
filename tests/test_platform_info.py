from agent_runtime_doctor import platform_info


def test_wsl_uses_os_release_when_environment_name_is_missing(monkeypatch) -> None:
    monkeypatch.delenv("WSL_INTEROP", raising=False)
    monkeypatch.delenv("WSL_DISTRO_NAME", raising=False)
    monkeypatch.setattr(platform_info.platform, "system", lambda: "Linux")
    monkeypatch.setattr(
        platform_info.platform,
        "release",
        lambda: "6.6.0-microsoft-standard-WSL2",
    )
    monkeypatch.setattr(platform_info.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(platform_info, "_linux_pretty_name", lambda: "Ubuntu 26.04 LTS")
    result = platform_info.detect_platform()
    assert result.wsl is True
    assert result.wsl_distribution == "Ubuntu 26.04 LTS"
