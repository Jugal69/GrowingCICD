import json
from pathlib import Path

from growingcicd.cli import main


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
