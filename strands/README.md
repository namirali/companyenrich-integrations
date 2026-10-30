# CompanyEnrich for strands

Strands no longer accepts new tools in strands-agents/tools. This package follows its community extension path. The official CompanyEnrich hosted MCP server is another supported option.

## Install from source

This package has not been published to PyPI. Install from the source repository:

```bash
pip install "git+https://github.com/namirali/companyenrich-integrations.git#subdirectory=strands"
```

Or, from this directory:

```bash
uv pip install -e .
export COMPANYENRICH_API_KEY="your-api-key"
```

Get a key from [CompanyEnrich](https://app.companyenrich.com/). An explicit `api_key` constructor argument takes precedence over the environment variable.

```python
from strands import Agent
from companyenrich_strands import CompanyEnrichTools

companyenrich = CompanyEnrichTools()
agent = Agent(tools=companyenrich.tools)
```

The tools expose `companyenrich_enrich_company(domain)`, `companyenrich_search_companies(semantic_query, page=1, page_size=5)`, and `companyenrich_similar_companies(domains, page=1, page_size=5)`. They return the original JSON object, including pagination and similarity metadata.

Each invocation makes one request. There is no automatic pagination or retry. The default HTTP timeout is 30 seconds, configurable with `timeout`. Search accepts a description of up to 500 characters, `page_size` from 1 to 100 and `page` starting at 1; `page * page_size` must not exceed 10,000 for search. Lookalikes accepts one to ten domains.

Enrichment costs 1 credit per call; search costs 1 credit per returned company (minimum 1); lookalikes costs 5 credits per returned company (minimum 5). The developer controls which tools to expose and the agent's budget. HTTP authentication, insufficient-credit, rate-limit and server failures propagate as `httpx.HTTPStatusError`. Timeouts propagate as `httpx.TimeoutException`. No API keys belong in agent prompts.

[API reference](https://docs.companyenrich.com/reference) · [MCP alternative](https://docs.companyenrich.com/docs/mcp-server)

## Development

```bash
uv venv --python 3.12
uv pip install -e ".[test]"
uv run --no-project pytest
uv run --no-project ruff check src tests
uv run --no-project ruff format --check src tests
uv build
```

Tests mock HTTP responses; no CompanyEnrich key, paid API call, or LLM is needed. Live authenticated behavior has not been tested. See `TESTING.md` for recorded verification.
