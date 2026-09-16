from __future__ import annotations

import argparse
import sys

from agent_runtime_doctor import __version__
from agent_runtime_doctor.doctor import collect_report
from agent_runtime_doctor.render import render_human, render_json, render_markdown


def _add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--no-native",
        action="store_true",
        help="skip provider-native diagnostic commands and only discover runtimes",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=45.0,
        metavar="SECONDS",
        help="per-command timeout (default: 45)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-runtime-doctor",
        description="Privacy-minimized, native-first diagnostics for coding-agent runtimes.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    doctor_parser = subparsers.add_parser("doctor", help="run diagnostics")
    _add_common_options(doctor_parser)
    doctor_parser.add_argument("--json", action="store_true", help="emit normalized JSON")

    report_parser = subparsers.add_parser("report", help="render a support report")
    _add_common_options(report_parser)
    report_parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="report format (default: markdown)",
    )
    return parser


def _validate_timeout(parser: argparse.ArgumentParser, timeout: float) -> None:
    if not 1.0 <= timeout <= 300.0:
        parser.error("--timeout must be between 1 and 300 seconds")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    _validate_timeout(parser, args.timeout)
    report = collect_report(run_native=not args.no_native, timeout=args.timeout)
    if args.command == "doctor":
        output = render_json(report) if args.json else render_human(report)
    else:
        output = render_json(report) if args.format == "json" else render_markdown(report)
    print(output)
    return 2 if report.overall_status == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
