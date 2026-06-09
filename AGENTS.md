# django-simple-starter — Agent Guide

## Project structure

```
dss/src/dss/          # package root (not dss/)
├── __init__.py       # __version__ = "0.2.1"
├── __main__.py       # python -m dss entrypoint
├── cli.py            # CLI entrypoint: dss.cli:main
└── generator.py      # DjangoProjectGenerator — all scaffold logic
pyproject.toml        # build config, scripts, dependencies
```

`dss/` at repo root is just a container for `src/`. The package source is at `dss/src/dss/`. Package discovery is configured with `[tool.setuptools.packages.find] where = ["dss/src"]`.

## Commands

- **Build**: `python -m build`
- **Install locally (editable)**: `pip install -e .`
- **Run CLI** (after editable install): `dss <project_name>`
- **Publish**: `twine upload dist/*` (uses credentials from `~/.pypirc`)

**CI publishes on GitHub release** (`.github/workflows/publish.yml`), not on push or tag.

## Versioning

Version is defined in **two places** that must stay in sync:
- `pyproject.toml` → `[project].version`
- `dss/src/dss/__init__.py` → `__version__`

Both need updating before publishing.

## Key facts

- **No tests** — no test framework configured, no test files.
- **No linter/formatter config** — `ruff` and `black` are dev dependencies but no config files exist (`ruff.toml`, `.pre-commit-config.yaml`, etc.).
- **PyPI re-upload rule** — same version + filename cannot be re-uploaded. If publishing a fix after a version is already live, bump the patch version.
- **Python >=3.10** required.
- **Entry point**: `dss = "dss.cli:main"` — single subcommand that takes a project name argument.
