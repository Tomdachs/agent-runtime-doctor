# Roadmap

The roadmap prioritizes independent usefulness and upstream-friendly diagnostics over feature count.

## v0.1 — native-first support report

- [x] versioned normalized schema;
- [x] platform/WSL facts without host identity;
- [x] Codex `doctor --json` normalization;
- [x] Claude Code and Gemini CLI discovery;
- [x] JSON and Markdown support reports;
- [x] bounded subprocesses and privacy regression tests;
- [ ] first tagged release after CI is green.

## v0.2 — broader structured adapters

- add provider-native structured diagnostics only where stable unattended output exists;
- add fixtures captured from documented schemas rather than private user state;
- distinguish provider-version compatibility from local environment health;
- document adapter support levels in a machine-readable matrix.

## v0.3 — automation

- GitHub Action for collecting a normalized CI-environment report;
- optional report-to-report diff for environment drift;
- standalone binaries so end users do not need Python installed.

## v1.0 — stable interchange contract

- stabilize adapter capability metadata and report schema;
- document compatibility/migration policy;
- require at least two provider-native structured diagnostic integrations or clearly document why a runtime cannot safely support unattended normalization.

## Non-goals

Automatic credential/ACL/sandbox repair, team policy management, agent routing, and replacing native provider diagnostics remain outside project scope.
