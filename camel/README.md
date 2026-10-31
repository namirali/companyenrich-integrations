# CompanyEnrich for camel

Prototype for human review. CAMEL requires an accepted prior discussion and meaningful human review before upstream issues/proposals/PRs. No upstream submission has been made.

## Install from source

This package has not been published to PyPI. Install from the source repository:

```bash
pip install "git+https://github.com/namirali/companyenrich-integrations.git#subdirectory=camel"
```

Or, from this directory:

```bash
uv pip install -e .
export COMPANYENRICH_API_KEY="your-api-key"
```

Get a key from [CompanyEnrich](https://app.companyenrich.com/). An explicit `api_key` constructor argument takes precedence over the environment variable.

```python
from camel.agents import ChatAgent
from companyenrich_camel import CompanyEnrichToolkit

toolkit = CompanyEnrichToolkit()
agent = ChatAgent(system_message="Research companies.", tools=toolkit.get_tools())
```

## Tools and responses

The package registers twelve core tools and one advanced operation selector:

| Tool | Capability |
| --- | --- |
| `companyenrich_enrich_company` | Domain enrichment; optional workforce expansion and wait_for_enrichment. |
| `companyenrich_search_companies` | Company search with semantic_query, literal query, structured filters, and optional workforce expansion. |
| `companyenrich_similar_companies` | Lookalikes from 1–10 domains with filters, workforce expansion, and wait_for_enrichment. |
| `companyenrich_search_people` | People search using full filters including query, companyFilter, roles, seniority, and education. |
| `companyenrich_lookup_person` | Email-to-person/company lookup with optional education expansion. |
| `companyenrich_company_workforce` | Workforce data using exactly one company_id UUID or domain. |
| `companyenrich_enrich_company_by_properties` | Match at least one documented name/social property. |
| `companyenrich_enrich_companies_batch` | Enrich 1–50 domains in one request; optional workforce expansion. |
| `companyenrich_get_company` | Get a company by UUID with optional workforce expansion. |
| `companyenrich_get_person` | Get a person by positive int64 ID, including a decimal string, with optional education expansion. |
| `companyenrich_count_companies` | Count a company search using semantic/literal queries and filters. |
| `companyenrich_count_similar_companies` | Count lookalikes from 1–10 seed domains with filters. |
| `companyenrich_advanced_operation` | One of 42 fixed API operations, including advanced discovery, taxonomy lookups, and job creation/status/listing. |

The original three names and positional arguments remain compatible. `companyenrich_search_companies(semantic_query, page=1, page_size=5)` retains its semantic description; the optional `query` keyword is a separate literal query. Search and lookalike tools accept structured `filters` that preserve all documented body fields and future nested fields. Dedicated inputs take precedence over filters, including default pagination.

Legacy core search/lookalike tools retain page size 5. People search also defaults to 5. Advanced company/person page searches default to page 1 and page size 10; advanced cursor requests default to page size 10. Page size must be 1–100; paginated company/person discovery windows cannot exceed 10,000 records. Literal queries allow 250 characters and semantic descriptions 500.

Responses retain all API fields, pagination metadata, similarity scores, and future nested fields. The original three tools return JSON objects; new operations also preserve arrays and numeric counts, including zero. There is no response projection. The companion async methods use an `a` prefix, for example `acompanyenrich_search_people` and `acompanyenrich_advanced_operation`.

```python
# Use the same toolkit instance created above.
result = toolkit.companyenrich_search_companies(
    "B2B software companies",
    query="software",
    filters={"countries": ["US"], "technologies": ["React"]},
)
people = toolkit.companyenrich_search_people(
    filters={"companyFilter": {"domains": ["example.com"]}, "positionQuery": ["engineer"]},
    expand=["education"],
)
```

## Advanced operations

`companyenrich_advanced_operation(operation, *, body=None, query=None, path_parameters=None, allow_beta=False)` exposes the 42 documented data, lookup, and job routes as an enum in the framework tool schema. It includes search/lookalike previews and counts, cursor scrolling, bulk enrichment, company and people exports, job status/listing, education, geographic lookups, and taxonomy/autocomplete endpoints. It excludes account details (`/me`) and saved-list administration.

The provider host, HTTP method, and path come from an internal allowlist; arbitrary URLs and custom authentication headers are not accepted. Three email operations are **Beta**: `get_people_email`, `post_people_email_bulk`, and `get_people_email_bulk_jobid`. Each requires explicit `allow_beta=True`.

```python
page = toolkit.companyenrich_advanced_operation(
    "post_companies_search_scroll",
    body={"query": "software", "pageSize": 10},
)
# Pass returned cursors explicitly for further pages. Jobs similarly require explicit status calls.
```

Each invocation makes one request. There is no automatic pagination, retry, polling, or result-URL downloading. Export creation requires an explicit count from 1 to 50,000; bulk company enrichment requires 1–10,000 domains, and beta bulk email creation requires 1–1,000 items. Job IDs, cursors, and result URLs are returned to the caller. Large person IDs remain exact in URL query strings and integer JSON request fields.

Data requests and optional expansions can consume credits. The caller controls which tools an agent receives and the request budget. Invalid input shapes, identifiers, expansions, bounds, and beta consent are checked before network access; CompanyEnrich remains authoritative for evolving filter semantics. Requests have a configurable 30-second default timeout and disabled redirects. HTTP failures remain `httpx.HTTPStatusError` with sanitized messages and response metadata; transport/timeout exception types are retained with sanitized messages. Errors do not expose API keys, request queries, or upstream response bodies. No API keys belong in agent prompts.

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

Tests mock HTTP responses; no CompanyEnrich key, paid API call, or LLM is needed. Live authenticated behavior has not been tested. The expanded suite checks all core routes and all 42 advanced operations, including synchronous and asynchronous execution through the available framework interfaces.

The package bounds MCP to 1.x and OpenAI below 3 to match CAMEL 0.2.90 imports. This avoids an incompatible MCP 2.x dependency resolution observed during verification.
