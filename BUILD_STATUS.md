# Integration build and coverage validation

Checked on 2026-10-31 after expanding all twelve native adapters to twelve core capabilities and a fixed advanced selector covering 42 HTTP operations. Existing branches and PRs were updated; package-registry publication and authenticated production calls were not performed. See [endpoint coverage](ENDPOINT_COVERAGE.md), [advanced operations](ADVANCED_OPERATIONS.md), and [target/submission status](TARGETS.md).

## Expanded source checks

Tests exercise actual platform registrations, all twelve core routes and all 42 advanced mappings with mocked HTTP. Coverage includes complete responses and metadata, zero counts, batch arrays, filters/expansions, exact large person IDs, strict beta opt-in, required fields/bounds, sanitized errors, and no unintended retries. Native Python async paths are covered where exposed. Additional tests use public framework invocation paths to catch input coercion before HTTP.

| Integration | Final local verification | Published source / review |
| --- | --- | --- |
| Activepieces | 78 tests and TypeScript build pass | [Source](activepieces) |
| Corsair | 78 tests; TypeScript, ESM bundle and declaration builds pass | [Source](corsair) |
| Dify | 104 tests; Ruff; official CLI packaging; all 12 local Marketplace checks pass. Archive contains 41 runtime/documentation files | [Source](dify), [draft PR #3576](https://github.com/langgenius/dify-plugins/pull/3576), `15e1cb5` |
| LlamaIndex | 258 tests; Ruff lint/format; wheel and sdist pass | [Source](llama-index), [verification](llama-index/TESTING.md) |
| Strands | 318 tests, including actual agent-stream execution of all operations and strict input validation; Ruff; wheel and sdist pass | [Source](strands), [verification](strands/TESTING.md) |
| CAMEL | 258 tests; actual sync/async registered tool calls; Ruff; wheel and sdist pass | [Source](camel), [verification](camel/TESTING.md) |
| Sim | 49 focused tests; scoped Biome; 13/13 canvas checks; block registry, generated metadata/docs/deployment catalog checks; 60 of 62 broad audits pass | [Draft PR #9485](https://github.com/simstudioai/sim/pull/9485), `8f676806` |
| Pipedream | 49 tests; ESLint; component build; official scoped key/app-property/duplicate validators pass using the actual component source | [Branch](https://github.com/namirali/pipedream/tree/codex/companyenrich-integration), `daa6917e` |
| Botpress | 129 tests; TypeScript, SDK build/lint and formatting pass | [Fork draft PR #1](https://github.com/namirali/botpress/pull/1), `863f3292` |
| CrewAI | 114 tests including real catalog extraction; five-module mypy check; Ruff; wheel and sdist pass | [PR #8844](https://github.com/crewAIInc/crewAI/pull/8844), `3d1d6946` |
| Langflow | 128 provider tests plus 163 migration tests (291 total); actual frontend/bundle registration; Ruff; migration guards; release plan; wheel and sdist pass | [PR #16078](https://github.com/langflow-ai/langflow/pull/16078), `ef3a1dd8` |
| Haystack | 210 tests pass, two live tests skipped; nine-module mypy check, Ruff, documentation generation, wheel and sdist pass | [Branch](https://github.com/namirali/haystack-core-integrations/tree/codex/companyenrich-integration), `932face9` |

The final review also repaired a missing generated Sim documentation entry, removed retained credentials/response bodies from legacy Haystack error objects, and prevented Haystack/Strands framework input coercion from bypassing numeric and beta-consent validation. Dify, CrewAI, Langflow, LlamaIndex and CAMEL also have explicit host-boundary checks. Haystack preserves its original opt-in retry setting for compatibility, defaulting to zero; new operations make one attempt.

## Check limits and upstream gates

- **Sim:** the full application typecheck produced no diagnostics before a 180-second deadline and was stopped. Full-repository `test-patterns` and `unused-exports` audits were stopped after approximately seven minutes without diagnostics. These three checks remain unverified; no complete production application build or live UI demo is claimed. Other listed checks passed. Fork Actions require maintainer approval and Vercel requires external-contributor authorization.
- **Pipedream:** the sparse checkout omits 1,250 unrelated app sources, so global key/app-property validation cannot complete. Unmodified official validators passed in an isolated fixture linked to the real CompanyEnrich source; the global duplicate-key check also passed. [App registration](https://github.com/PipedreamHQ/pipedream/issues/22385) remains necessary before an upstream PR.
- **Dify:** the PR remains a draft pending real Dify deployment/remote-debugging validation. Remote package precheck requires maintainer approval. Local warnings concern the manifest's network-domain declaration, unpinned dependencies/offline vulnerability lookup, and a scanner heuristic that mistakes the HTTP dispatcher's `execute` name for possible SQL. There is no database execution in that dispatcher. No blocking local package findings remain.
- **Haystack:** no upstream PR was opened because live validation and proposal acceptance remain outstanding. Workflow files were not pushed because the credential lacks workflow scope; the [inert CI patch](haystack/upstream-ci.patch) remains review material, not active CI. The existing two live smoke tests only cover domain enrichment.
- **Botpress:** the updated PR is in the contributor fork; upstream PR creation permission remains unavailable.
- **CrewAI/Langflow:** new remote runs are pending or require maintainer authorization. Local checks listed above passed; full local monorepo suites are not claimed. CrewAI still requires the maintainer's AI-contribution label. Langflow's early expansion run again hit the known Valkey/Python 3.15 baseline dependency failure. Earlier unrelated Python 3.15 Toolguard/LiteLLM, pandas/MarkItDown and Docker runner-export failures are recorded in prior history; new remote runs must be assessed independently.

## Existing proxy and MCP artifacts

Nango and MCP connections already provide generic proxy or dynamic tool discovery, so no redundant REST wrappers were added. Their earlier verified implementations remain unchanged.

| Artifact | Verification / current limits |
| --- | --- |
| [Nango PR #8118](https://github.com/NangoHQ/nango/pull/8118) | Official provider validator passes locally; posted checks pass or are neutral. Twelve Actions workflows require maintainer approval. |
| [AutoGPT PR #16447](https://github.com/Significant-Gravitas/AutoGPT/pull/16447) | Earlier 74 catalog tests and 70 MCP logo assertions pass. Current remote snapshot has 55 successful checks; the CLA check now succeeds. Vercel authorization remains the failing external status. |
| [LangChain](langchain) | Actual `MCPAdapter` tool discovery passed against an in-process FastMCP fixture; URL and bearer authentication checked. Tested with LangChain 1.4.7/FastMCP 4.1.4. |
| [Mastra](mastra) | Actual example initialized, authenticated, listed tools and disconnected from a local HTTP MCP fixture. Tested with `@mastra/mcp` 2.7.0; requires Node.js 22.13+. |
| [Windmill](windmill) | Resource JSON and configured URL/credential placeholder verified. No deployment performed. |
| [MCP Registry](mcp-registry) | Manifest passed the referenced official JSON schema. Namespace verification/publication remain outstanding. |
| [MCP directories](mcp-directories) | Submission metadata parses; website/listing prerequisites remain outstanding. |

Local MCP fixture tests verify interoperability, not the authenticated hosted server's live tool inventory. No live authenticated or credit-consuming CompanyEnrich requests, LLM calls, or npm/PyPI publications were made. A successful local build does not imply upstream acceptance or completed deployment testing.

Dify package SHA256: `0d190a614a3f648956ee3c7cfa30a256ecc0948aec54e2188eadac34afb77262`.
