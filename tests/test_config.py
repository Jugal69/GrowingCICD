import json
from pathlib import Path

import pytest

from growingcicd.cli import main
from growingcicd.config import validate_config


def test_example_config_is_valid() -> None:
    example_path = Path(__file__).parents[1] / "config.example.json"

    assert validate_config(json.loads(example_path.read_text(encoding="utf-8"))) == []


@pytest.mark.parametrize(
    ("config", "expected_error"),
    [
        ([], "configuration must be a JSON object"),
        (
            {"name": "service", "environment": "staging", "port": 8080},
            "'environment' must be one of: development, production, testing",
        ),
        (
            {"name": "service", "environment": [], "port": 8080},
            "'environment' must be one of: development, production, testing",
        ),
        (
            {"name": "service", "environment": "testing", "port": True},
            "'port' must be an integer between 1 and 65535",
        ),
        (
            {"name": " ", "environment": "testing", "port": 8080},
            "'name' must be a non-empty string",
        ),
    ],
)
def test_validate_config_reports_invalid_values(config: object, expected_error: str) -> None:
    assert expected_error in validate_config(config)


def test_cli_writes_success_report(tmp_path: Path) -> None:
    example_path = Path(__file__).parents[1] / "config.example.json"
    report_path = tmp_path / "reports" / "validation-report.json"

    result = main([str(example_path), "--report", str(report_path)])

    assert result == 0
    assert json.loads(report_path.read_text(encoding="utf-8")) == {
        "config": str(example_path),
        "valid": True,
        "errors": [],
    }


def test_cli_writes_failure_report(tmp_path: Path) -> None:
    config_path = tmp_path / "invalid.json"
    report_path = tmp_path / "validation-report.json"
    config_path.write_text('{"name": "service"}', encoding="utf-8")

    result = main([str(config_path), "--report", str(report_path)])

    assert result == 1
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["valid"] is False
    assert len(report["errors"]) == 2
