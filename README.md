# GrowingCICD

A small Python package that validates JSON configuration and demonstrates a
Pixi-based CI pipeline.

## Run locally

Install [Pixi](https://pixi.sh/latest/) and run the checks from the repository
root:

```sh
pixi run ci
```

This runs Ruff linting, the pytest suite, and validation of
[`config.example.json`](./config.example.json). The validation report is written
to `reports/validation-report.json`.

The example configuration requires a non-empty `name`, an `environment` of
`development`, `testing`, or `production`, and an integer `port` between 1 and
65535. To validate another JSON file and choose a report path:

```sh
pixi run validate-config path/to/config.json --report reports/custom-report.json
```

GitHub Actions runs the same checks when a pull request is opened or updated
and when code is pushed to `main`. The generated validation report is uploaded
as the `validation-report` workflow artifact, including when another check
fails.
