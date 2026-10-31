# CompanyEnrich endpoint coverage

Audited on 2026-10-31 against the current public API reference and the actual action/tool registrations, request builders, and response parsers in the prepared submissions. The reference contains **48 documented HTTP operations**, recorded with source URLs and input fields in [api-endpoints.json](api-endpoints.json). This is an inventory, not a recommendation to expose every administrative operation in every agent.

**The prepared integrations do not provide complete product coverage.** Eleven native adapters expose three company operations; Haystack exposes one. Nango provides generic API access, while the MCP connections inherit the hosted server's tool inventory. The earlier [build audit](BUILD_STATUS.md) verified builds and tests, not endpoint completeness. This audit does not add endpoints or claim live authenticated validation.

## What “enrichment only” means in each case

- **Haystack really is enrichment only.** The [submitted proposal](https://github.com/deepset-ai/haystack-core-integrations/issues/4179) explicitly limits the first contribution to domain enrichment and defers search/lookalikes. This was a submission scope choice, not a demonstrated platform restriction.
- **Sim has three operations.** Its operation selector defaults to enrichment; search and lookalikes are also wired. Seeing enrichment selected does not mean the other two are missing.
- **Nango is an authentication and proxy provider.** Its `/me` quickstart is a credential example. Callers can supply other CompanyEnrich paths, methods, parameters, and bodies through Nango's proxy. It has no prebuilt CompanyEnrich actions or syncs and no CompanyEnrich-specific endpoint allowlist.
- **MCP entries are server connections.** They discover tools rather than hardcode REST endpoints. They should not be assessed by counting native REST calls in the connector source.

The three-action scope is visible in the native implementations and documentation, and the implemented actions are registered. The absent endpoint families are therefore mainly unimplemented features from the initial limited scope, rather than forgotten action registrations. There is no documented platform requirement that makes people, workforce, or the other useful operations impossible. Calling these complete CompanyEnrich integrations would overstate their coverage.

## Native adapters, one by one

“Three” below means `GET /companies/enrich`, `POST /companies/search`, and `POST /companies/similar`. An internal `/me` credential probe is not an additional data feature. None of these native adapters exposes a public, general-purpose CompanyEnrich API request action.

| Integration | Data operations | Search and lookalike input coverage | Source |
| --- | --- | --- | --- |
| Sim | Three | Literal name/domain query; one lookalike seed | [PR #9485](https://github.com/simstudioai/sim/pull/9485) |
| Pipedream | Three | Literal query, countries, keywords; 1–10 seeds and countries/keywords for lookalikes | [Source branch](https://github.com/namirali/pipedream/tree/codex/companyenrich-integration/components/companyenrich) |
| Botpress | Three | Semantic query; 1–10 seeds; no structured search filters | [Fork PR #1](https://github.com/namirali/botpress/pull/1) |
| Activepieces | Three | Literal name/domain query; one seed | [Registration](activepieces/src/index.ts), [inputs](activepieces/src/lib/actions/discover-companies.ts) |
| Corsair | Three | Literal query, countries, keywords; 1–10 seeds | [Registration](corsair/index.ts), [schemas](corsair/endpoints/types.ts) |
| Dify | Three | Semantic query; 1–10 seeds; no structured search filters | [Registration](dify/provider/companyenrich.yaml), [client](dify/common/client.py) |
| CrewAI | Three | Semantic query; 1–10 seeds; no structured search filters | [PR #8844](https://github.com/crewAIInc/crewAI/pull/8844) |
| Langflow | Three | Optional semantic query plus a Filters object for other search body fields; lookalike Filters also supported | [PR #16078](https://github.com/langflow-ai/langflow/pull/16078) |
| Haystack | Domain enrichment only | Component and agent-tool wrapper call the same endpoint; no search/lookalikes | [Source branch](https://github.com/namirali/haystack-core-integrations/tree/codex/companyenrich-integration/integrations/companyenrich) |
| LlamaIndex | Three | Semantic query; 1–10 seeds; no structured search filters | [Tool specification](llama-index/src/llama_index/tools/companyenrich/base.py) |
| Strands | Three | Semantic query; 1–10 seeds; no structured search filters | [Registered tools](strands/src/companyenrich_strands/__init__.py) |
| CAMEL | Three | Semantic query; 1–10 seeds; no structured search filters | [Toolkit](camel/src/companyenrich_camel/__init__.py) |

## Coverage gaps inside implemented endpoints

The current company search schema has 29 body fields, including literal and semantic queries, geography, employee/revenue ranges, funding, technologies, exclusions, and workforce filters. Most wrappers expose only query text and pagination. Langflow can pass additional body fields through its Filters input; this does not add other endpoints. [Search reference](https://docs.companyenrich.com/reference/post_companies-search)

The native wrappers do not expose the documented `expand=workforce` response option, or the relevant `waitForEnrichment` options on enrichment/lookalikes. Langflow's workforce filtering is distinct from retrieving the workforce expansion. Returning an ordinary company profile is also not equivalent to calling the workforce API. [Enrichment](https://docs.companyenrich.com/reference/get_companies-enrich), [lookalikes](https://docs.companyenrich.com/reference/post_companies-similar), [workforce](https://docs.companyenrich.com/reference/get_companies-workforce)

Response coverage is uneven too:

- Sim and Corsair project company profiles to ten fields, so other returned fields are discarded. Sim retains similarity scores through a flattened output; Corsair retains page and score metadata. [Sim parser](https://github.com/simstudioai/sim/blob/31444f9179ca9c2c88e0630bbff4b6643d5bd77a/apps/sim/tools/companyenrich/utils.ts), [Corsair schema](corsair/endpoints/types.ts)
- Pipedream discovery returns company arrays but omits pagination metadata and similarity scores. That limitation is documented in its current README. [Pipedream source](https://github.com/namirali/pipedream/tree/codex/companyenrich-integration/components/companyenrich)
- Botpress, Activepieces, Dify, and the audited Python adapters preserve raw response objects, but that does not make unrequested expansions or unimplemented endpoints available.

Python `async` methods call the same REST endpoints asynchronously; they do not implement CompanyEnrich's background export or bulk-job APIs. Multiple lookalike seed domains are not batch enrichment.

## Useful missing capabilities and suggested scope

These priorities are recommendations from this audit, not features already implemented. They apply to native adapters; Nango can already proxy these routes and MCP coverage depends on the server.

| Capability | Current native coverage | Recommendation and official reference |
| --- | --- | --- |
| Company search/lookalikes in Haystack | Missing | Add separate discovery components/tools if the contribution expands beyond an enricher. |
| Rich company search and similarity controls | Partial | Support literal and semantic search, structured filters, and relevant request options consistently. [Search](https://docs.companyenrich.com/reference/post_companies-search), [similar](https://docs.companyenrich.com/reference/post_companies-similar) |
| People search and reverse-email/person lookup | Missing in all 12 native adapters | High priority for prospecting, CRM, and agent workflows. [People search](https://docs.companyenrich.com/reference/post_people-search), [lookup](https://docs.companyenrich.com/reference/post_people-lookup) |
| Workforce/headcount retrieval | Missing in all 12 | Add the dedicated operation and explicit expansion options where appropriate. [Workforce](https://docs.companyenrich.com/reference/get_companies-workforce) |
| Enrich by name/social properties and fetch by ID | Missing in all 12 | Useful when a domain is unavailable or a previous result already supplies an ID. [Properties](https://docs.companyenrich.com/reference/post_companies-enrich), [company ID](https://docs.companyenrich.com/reference/get_companies), [person ID](https://docs.companyenrich.com/reference/get_people) |
| Batch company enrichment | Missing in all 12 | High value for workflow and pipeline hosts; support the documented 1–50 domain batch. [Batch](https://docs.companyenrich.com/reference/post_companies-enrich-batch) |
| Search/lookalike counts and previews | Missing in all 12 | Counts help estimate result sets; previews need explicit plan handling because they require Scale. [Count](https://docs.companyenrich.com/reference/post_companies-search-count), [similar count](https://docs.companyenrich.com/reference/post_companies-similar-count), [preview](https://docs.companyenrich.com/reference/post_companies-search-preview), [similar preview](https://docs.companyenrich.com/reference/post_companies-similar-preview) |
| Cursor-based company/people/lookalike retrieval | Missing in all 12 | Add explicit cursor operations for large datasets; keep page limits and credit use visible. [Company scroll](https://docs.companyenrich.com/reference/post_companies-search-scroll), [people scroll](https://docs.companyenrich.com/reference/post_people-search-scroll), [similar scroll](https://docs.companyenrich.com/reference/post_companies-similar-scroll) |
| Bulk enrichment and async exports | Missing in all 12 | Best suited to workflow/pipeline integrations. Implement create, status, and result handling together rather than expose only job creation. [Bulk](https://docs.companyenrich.com/reference/post_companies-enrich-bulk), [company export](https://docs.companyenrich.com/reference/post_companies-search-async), [people export](https://docs.companyenrich.com/reference/post_people-search-async) |
| Work-email resolution, bulk email, education | Missing in all 12 | Useful optional people capabilities; email endpoints are explicitly beta and need status handling. [Email](https://docs.companyenrich.com/reference/get_people-email), [bulk email](https://docs.companyenrich.com/reference/post_people-email-bulk), [education](https://docs.companyenrich.com/reference/get_people-education) |
| Saved lists, autocomplete, geography and taxonomies | Missing as data features | Add where the host's workflow or input UI benefits; not every agent needs list management. Exact operations are in [the inventory](api-endpoints.json). |

The existing explicit pagination and absence of automatic paid retries are separate design choices worth retaining. They are not reasons to omit people or workforce support.

The public `/jobs` routes manage asynchronous API jobs, **not job postings**. Job-posting and ad-intelligence product routes were not present in this 48-operation public reference, so no route should be invented for them. Funding is already represented in company data and search fields; a separate funding endpoint was not found in this reference. [API index](https://docs.companyenrich.com/llms.txt), [jobs reference](https://docs.companyenrich.com/reference/get_jobs)

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

## Audit limits

Source coverage was checked at the existing submitted commits, including registration and output behavior. The current documentation was read without making authenticated or credit-consuming API requests. No product entitlement or live result behavior was inferred from successful builds. Only documentation and the API inventory changed in this audit; implementation expansion remains outstanding.
