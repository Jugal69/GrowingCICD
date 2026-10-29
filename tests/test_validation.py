import json
from pathlib import Path

import pytest

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


@pytest.mark.parametrize("port", [1, 65535])
def test_validate_config_accepts_port_boundaries(port: int) -> None:
    config = {"name": "service", "environment": "testing", "port": port}

    assert validate_config(config) == []


@pytest.mark.parametrize("port", [0, -1, 65536, 8080.5, None])
def test_validate_config_rejects_invalid_ports(port: object) -> None:
    config = {"name": "service", "environment": "testing", "port": port}

    assert validate_config(config) == ["'port' must be an integer between 1 and 65535"]
