# Security policy

## Reporting a vulnerability

Please do not open a public issue for a vulnerability that could expose credentials, private paths, authentication state, or allow unexpected command execution.

Use GitHub's private vulnerability reporting for this repository when available. If that channel is unavailable, contact the repository owner privately through the GitHub profile before disclosing details publicly.

## Security design expectations

- diagnostic commands are read-only by default;
- subprocesses use argument arrays, not a shell;
- subprocess runtime and captured output are bounded;
- secret values and raw environment-variable values are never rendered;
- native diagnostic output is allowlisted into a normalized schema;
- executable paths are not included in public support reports.

A report that merely detects the *presence* of a sensitive configuration mechanism is not itself a reason to reveal the configuration value.
