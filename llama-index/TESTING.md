# Verification record

Verified on 2026-10-31 with Python 3.12 on macOS against llama-index-core 0.14.25.

- `pytest -q`: 45 passed. HTTP responses are mocked with respx; framework tool schemas and dispatch use the actual installed framework.
- `ruff check src tests` and `ruff format --check src tests`: passed.
- `uv build`: wheel and source distribution built successfully.

Coverage includes sync/async request authentication and payloads, pagination metadata, invalid arguments, missing credentials, HTTP redirects and 401/402/429/500 errors, timeouts, response shape, and framework dispatch. Requests are bounded to one page and are never retried automatically.

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
