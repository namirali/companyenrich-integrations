# Verification record

Verified on 2026-10-31 with Python 3.12 on macOS against strands-agents 1.63.0.

- `pytest -q`: 318 passed. HTTP responses are mocked with respx; framework tool schemas and dispatch use the actual installed framework.
- `ruff check src tests` and `ruff format --check src tests`: passed.
- `uv build --offline`: wheel and source distribution built successfully.

Coverage includes all twelve core routes and 42 advanced mappings, actual framework registry dispatch, sync/async requests, full response preservation, counts including zero, arrays, large int64 IDs, filters/expansions, beta opt-in, pagination and batch/seed/export limits, invalid inputs before HTTP, credentials, redirects and 401/402/429/500 errors, timeouts, sanitized errors, and serialization. Requests are bounded to one page and are never retried automatically.

No live authenticated CompanyEnrich request, paid API call, LLM call, PyPI publication, or upstream framework submission was performed. Other Python versions and operating systems have not been tested.

## Reproduce

```bash
uv venv --python 3.12
uv pip install -e ".[test]"
uv run --no-project pytest -q
uv run --no-project ruff check src tests
uv run --no-project ruff format --check src tests
uv build
```
