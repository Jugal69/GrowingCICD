"""Validation for the example application's JSON configuration."""

ENVIRONMENTS = {"development", "testing", "production"}


def validate_config(config: object) -> list[str]:
    """Return validation errors for a decoded JSON configuration value."""
    if not isinstance(config, dict):
        return ["configuration must be a JSON object"]

    errors: list[str] = []
    name = config.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("'name' must be a non-empty string")

    environment = config.get("environment")
    environment_is_valid = isinstance(environment, str) and environment in ENVIRONMENTS
    if not environment_is_valid:
        errors.append(f"'environment' must be one of: {', '.join(sorted(ENVIRONMENTS))}")

    port = config.get("port")
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        errors.append("'port' must be an integer between 1 and 65535")

    if environment_is_valid and environment == "production":
        deployment = config.get("deployment")
        if not isinstance(deployment, dict):
            errors.append("'deployment' must be an object for production")
        else:
            replicas = deployment.get("replicas")
            if isinstance(replicas, bool) or not isinstance(replicas, int) or replicas < 1:
                errors.append("'deployment.replicas' must be a positive integer")

            health_check = deployment.get("health_check")
            if not isinstance(health_check, dict):
                errors.append("'deployment.health_check' must be an object")
            else:
                path = health_check.get("path")
                if not isinstance(path, str) or not path.startswith("/") or not path.strip():
                    errors.append("'deployment.health_check.path' must be a non-empty absolute path")

                interval_seconds = health_check.get("interval_seconds")
                if (
                    isinstance(interval_seconds, bool)
                    or not isinstance(interval_seconds, int)
                    or interval_seconds < 1
                ):
                    errors.append(
                        "'deployment.health_check.interval_seconds' must be a positive integer"
                    )

            startup_command = deployment.get("startup_command")
            if not isinstance(startup_command, str) or not startup_command.strip():
                errors.append("'deployment.startup_command' must be a non-empty string")
    elif environment_is_valid and "deployment" in config:
        errors.append("'deployment' is only allowed when 'environment' is 'production'")

    return errors
