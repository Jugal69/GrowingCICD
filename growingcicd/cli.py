"""Command-line interface for validating a JSON configuration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from growingcicd.config import validate_config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a JSON configuration file.")
    parser.add_argument("config", type=Path, help="path to the JSON configuration")
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/validation-report.json"),
        help="path for the JSON validation report",
    )
    args = parser.parse_args(argv)

    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"error: cannot read configuration '{args.config}': {error}", file=sys.stderr)
        return 2

    errors = validate_config(config)
    report = {
        "config": str(args.config),
        "valid": not errors,
        "errors": errors,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(f"{json.dumps(report, indent=2)}\n", encoding="utf-8")

    if errors:
        for error in errors:
            print(f"Invalid configuration: {error}", file=sys.stderr)
        return 1

    print(f"Configuration is valid. Report written to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
