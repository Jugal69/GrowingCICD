"""Validation for the example application's JSON configuration."""

ENVIRONMENTS = {"development", "testing", "production"}


def validate_config(config: object) -> list[str]:
    """Return validation errors for a decoded JSON configuration value."""
    if not isinstance(config, dict):
        return ["configuration must be a JSON object"]

    errors = []
    name = config.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("'name' must be a non-empty string")

    environment = config.get("environment")
    if not isinstance(environment, str) or environment not in ENVIRONMENTS:
        errors.append(f"'environment' must be one of: {', '.join(sorted(ENVIRONMENTS))}")

    port = config.get("port")
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        errors.append("'port' must be an integer between 1 and 65535")

    return errors
