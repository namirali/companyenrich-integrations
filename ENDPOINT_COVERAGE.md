# CompanyEnrich endpoint coverage

Expanded on 2026-10-31 against the public API reference. The twelve native adapters now provide **twelve core capabilities plus an explicit advanced selector covering 42 HTTP operations in total**. The full reference has 48 operations: five saved-list administration routes are intentionally outside this scope, and `GET /me` remains credential-validation-only. The advanced selector includes the twelve core routes; these are not 54 distinct endpoints.

The earlier implementation scope was too narrow: eleven native adapters had three company operations, and Haystack had one. Successful builds did not establish product coverage. This expansion adds the missing useful data capabilities, rich inputs, and response preservation. See [the complete 48-operation inventory](api-endpoints.json), [the 42-operation selector](ADVANCED_OPERATIONS.md), and [validation and remaining gates](BUILD_STATUS.md).

## Core capabilities

| Capability | HTTP operation | Inputs and output |
| --- | --- | --- |
| Domain enrichment | `GET /companies/enrich` | Domain; optional workforce expansion and wait-for-enrichment; full profile |
| Company search | `POST /companies/search` | Literal/semantic query, structured filters, explicit page; full metadata |
| Lookalikes | `POST /companies/similar` | 1–10 domains, structured filters, supported expansion/wait options; scores retained |
| People search | `POST /people/search` | Structured people/company filters, explicit page and education expansion |
| Email-to-person lookup | `POST /people/lookup` | Email and optional education expansion |
| Workforce | `GET /companies/workforce` | Exactly one company UUID or domain |
| Enrich by matching properties | `POST /companies/enrich` | At least one documented name/social property; optional workforce expansion |
| Batch enrichment | `POST /companies/enrich/batch` | 1–50 domains; array response preserved |
| Company by ID | `GET /companies` | Company UUID; supported expansion |
| Person by ID | `GET /people` | Positive int64 ID, including decimal strings to avoid JavaScript precision loss |
| Company count | `POST /companies/search/count` | Search filters; preserves zero |
| Lookalike count | `POST /companies/similar/count` | 1–10 seed domains and filters; preserves zero |

Native adapters expose these through their actual framework registries. Existing public names and core defaults are preserved. Some Python adapters retain their existing five-result default; other core actions default to ten. The advanced page-based search defaults explicitly to page 1 and size 10.

## Native adapters

| Integration | Implemented coverage | Source / review |
| --- | --- | --- |
| Sim | Twelve core operations plus advanced selector; full response data retained alongside compatible outputs | [PR #9485](https://github.com/simstudioai/sim/pull/9485) |
| Pipedream | Twelve core actions plus advanced selector; legacy discovery arrays retained with full page/metadata companion exports | [Source branch](https://github.com/namirali/pipedream/tree/codex/companyenrich-integration/components/companyenrich) |
| Botpress | Twelve core actions plus advanced selector; complete JSON output envelopes | [Fork PR #1](https://github.com/namirali/botpress/pull/1) |
| Activepieces | Twelve core actions plus advanced selector; complete response values | [Registration](activepieces/src/index.ts), [actions](activepieces/src/lib/actions/catalog.ts) |
| Corsair | Twelve core data methods plus advanced selector; company/page schemas retain additional fields | [Registration](corsair/index.ts), [schemas](corsair/endpoints/types.ts) |
| Dify | Twelve core tools plus advanced selector; arrays/numbers wrapped as `data` for Dify JSON messages | [Provider](dify/provider/companyenrich.yaml), [PR #3576](https://github.com/langgenius/dify-plugins/pull/3576) |
| CrewAI | Twelve core tools plus advanced selector, including catalog exports | [PR #8844](https://github.com/crewAIInc/crewAI/pull/8844) |
| Langflow | Twelve core components plus advanced selector, including migration and release registration | [PR #16078](https://github.com/langflow-ai/langflow/pull/16078) |
| Haystack | Existing enricher retained; discovery, people, counts and advanced operations added | [Source branch](https://github.com/namirali/haystack-core-integrations/tree/codex/companyenrich-integration/integrations/companyenrich) |
| LlamaIndex | Twelve core tools plus advanced selector, synchronous and asynchronous | [Tool specification](llama-index/src/llama_index/tools/companyenrich/base.py) |
| Strands | Twelve core tools plus advanced selector | [Registered tools](strands/src/companyenrich_strands/__init__.py) |
| CAMEL | Twelve core tools plus advanced selector | [Toolkit](camel/src/companyenrich_camel/__init__.py) |

Search filters are JSON objects, so callers can supply geography, funding, workforce, technology, exclusions and other documented fields. Dedicated parameters take precedence. Unknown evolving body fields are preserved for server validation; unknown query and path parameters are rejected to catch mistakes. Supported `expand` options are exposed separately. Full API responses retain future nested fields, page metadata and similarity scores; Pipedream and Sim retain compatible legacy outputs alongside complete data.

## Advanced operations and deliberate limits

The fixed selector also covers search/lookalike previews, company/people/lookalike scroll, bulk enrichment, company/people export jobs, job status/list operations, work-email resolution, bulk email/status, education, geography, industries and autocomplete. Each route is documented in [ADVANCED_OPERATIONS.md](ADVANCED_OPERATIONS.md).

- New actions and default configurations make one request per invocation. No automatic pagination, job polling, or result-URL downloading occurs. Returned status/result URLs remain data. Haystack retains its legacy explicitly configured retry option; the default remains zero and all new operations make one attempt.
- Beta email operations require `allow_beta=true`. Provider entitlements and credit charges still apply; preview availability depends on the plan.
- Export jobs require an explicit count, capped at 50,000. The public prose says 50,000 while the OpenAPI schema permits a larger value; the adapters choose the conservative limit.
- Page size is 1–100 and page-based search is capped at 10,000 results. Batch enrichment accepts 1–50 domains; lookalikes accept 1–10 seeds. Larger workloads use explicit bulk/scroll operations.
- Saved-list administration is intentionally excluded. `/me` can contain account secrets and is never a public data action.
- `/jobs` manages background API jobs, not job postings. The audited public reference contains no separate advertising or job-posting product routes, so none were invented. Funding is available in company data and search filters.

## Proxy and MCP coverage

| Artifact | Actual coverage |
| --- | --- |
| Nango | Generic authenticated CompanyEnrich API proxy; no prebuilt endpoint actions or syncs. [Provider PR](https://github.com/NangoHQ/nango/pull/8118) |
| AutoGPT | Hosted MCP catalog entry. Generic discovery supplies tools and their input schemas. The five entries in `mcp_effects.json` classify tool effects; they are not an allowlist. [PR](https://github.com/Significant-Gravitas/AutoGPT/pull/16447) |
| LangChain | `MCPAdapter.list_tools()` discovers the hosted tools; no connector-side three-tool limit. [Example](langchain/list_tools.py) |
| Mastra | `MCPClient.listTools()` discovers the hosted tools; no CompanyEnrich-specific allowlist. [Example](mastra/list-tools.mjs) |
| Windmill | Hosted MCP resource configuration; actual available tools and user-configured filters are determined in Windmill. [Resource](windmill/companyenrich.resource.json) |
| MCP Registry | Prepared server connection metadata, not an implementation of REST endpoints. [Manifest](mcp-registry/server.json) |
| MCP directories | Prepared listing metadata, not executable endpoint implementations. [Submission](mcp-directories/submission.json) |

The [MCP setup guide](https://docs.companyenrich.com/docs/mcp-server) describes three company capabilities, while the [AI-agents product page](https://companyenrich.com/solutions/ai-agents) also documents people search and reverse email. Authenticated `tools/list` and schemas were not available for this audit. Therefore MCP connections cannot currently be certified as exposing all 48 REST operations, or any specific unverified server tool. The local MCP fixture tests verified client interoperability, not the live server's feature inventory.

## Validation limits

Coverage is verified through source inspection, framework registry tests, mocked routing/response tests, package builds and applicable contribution checks. All 42 advanced mappings and twelve core routes are exercised locally. Mocked tests verify behavior without consuming credits; they do not establish live API behavior, plan entitlements or Marketplace deployment readiness. Upstream approval, contributor policies and required live tests remain distinct from code completion.
