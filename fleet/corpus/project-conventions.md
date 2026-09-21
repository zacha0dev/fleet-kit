# Project conventions

- **Language:** Python 3.11, standard library plus `pytest`. *Source: `pyproject.toml`.*
- **Tests:** `python -m pytest -q`. A test file mirrors its module: `sample_app/x.py` → `tests/test_x.py`. *Source: repository layout, 2026-09-21.*
- **Branches:** `main` is the trunk. Work lands by pull request. Fleet changes are titled `reinforce: …` or `fleet: …`. *Source: `.github/copilot-instructions.md`.*
- **Versioning:** semantic; the changelog decides the bump. *Source: `release-checklist` skill.*
