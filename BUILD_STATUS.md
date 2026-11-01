# Integration build and coverage validation

Status checked on 2026-11-01; local implementation validation below records the 2026-10-31 expansion of all twelve native adapters to twelve core capabilities and a fixed advanced selector covering 42 HTTP operations. Existing branches and PRs were updated; package-registry publication and authenticated production calls were not performed. See [endpoint coverage](ENDPOINT_COVERAGE.md), [advanced operations](ADVANCED_OPERATIONS.md), and [target/submission status](TARGETS.md).

## Latest PR follow-up

Rechecked on 2026-11-01 at approximately 17:24 Europe/Istanbul (14:24 UTC). No new runtime defect or review request required a code fix. Six upstream PRs remain open. [Botpress fork PR #1](https://github.com/namirali/botpress/pull/1) was merged by `namirali` into `namirali/botpress:master` at 11:00 UTC, merge commit `ccf9cc63`; no matching upstream Botpress PR was found. The source head and prior passing validation are unchanged.

Dify's upstream package precheck still passes, including dependency installation and packaging. CrewAI's Bugbot, Cursor security and linked-issue checks pass on `bef3344a`; test/type/lint workflows await maintainer authorization. Langflow still has 223 successful checks, 12 skipped and exactly the same 12 failed job URLs described below. Nango, AutoGPT and Sim retain their existing approval/deployment gates; Pipedream, Corsair, Agno and Haystack proposals have no new replies. Unchanged runtime suites were not repeated in this status-only sweep.

Documentation was corrected to distinguish recommendations from submission requirements: Haystack proposal approval is not an explicit prerequisite for opening a PR, and Corsair maintainer assignment is recommended. Live validation, CI publication and the other concrete requirements below remain outstanding.

Rechecked reviews, inline comments and CI on 2026-10-31. CrewAI's automated review identified a malformed-JSON error-handling bug: reconstructing Requests' JSONDecodeError with one argument raised a TypeError. Commit `bef3344a` separates JSON decoding from transport errors and raises sanitized errors outside the exception handler so the original request/response cannot remain in the exception chain. Eight regression cases exercise real empty/HTML responses and HTTPError/Timeout failures through public core and advanced tool calls. All 122 provider tests, scoped lint/types and package builds pass; independent review found no remaining issue in this fix.

No new source changes were requested on Nango, AutoGPT, Dify, Sim, Pipedream or Botpress. Botpress also passed a fresh 129-test suite, typecheck, formatting, SDK lint and build. Pipedream, Corsair, Agno and Haystack proposals remain open without maintainer replies. GitHub reported no Actions runs for the standalone repository; its validation remains local. Existing live-testing and submission requirements below still apply.

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
| Botpress | 129 tests; TypeScript, SDK build/lint and formatting pass | [Merged fork PR #1](https://github.com/namirali/botpress/pull/1), source `863f3292` |
| CrewAI | 122 tests including real catalog extraction and malformed-JSON/transport-error regressions; five-module mypy check; Ruff; wheel and sdist pass | [PR #8844](https://github.com/crewAIInc/crewAI/pull/8844), `bef3344a` |
| Langflow | 128 provider tests plus 163 migration tests (291 total); actual frontend/bundle registration; Ruff; migration guards; release plan; wheel and sdist pass | [PR #16078](https://github.com/langflow-ai/langflow/pull/16078), `ef3a1dd8` |
| Haystack | 210 tests pass, two live tests skipped; nine-module mypy check, Ruff, documentation generation, wheel and sdist pass on runtime `932face9`; README-only correction `b60bc784` | [Branch](https://github.com/namirali/haystack-core-integrations/tree/codex/companyenrich-integration) |

The final review also repaired a missing generated Sim documentation entry, removed retained credentials/response bodies from legacy Haystack error objects, and prevented Haystack/Strands framework input coercion from bypassing numeric and beta-consent validation. Dify, CrewAI, Langflow, LlamaIndex and CAMEL also have explicit host-boundary checks. Haystack preserves its original opt-in retry setting for compatibility, defaulting to zero; new operations make one attempt.

## Check limits and upstream gates

- **Sim:** the full application typecheck produced no diagnostics before a 180-second deadline and was stopped. Full-repository `test-patterns` and `unused-exports` audits were stopped after approximately seven minutes without diagnostics. These three checks remain unverified; no complete production application build or live UI demo is claimed. Other listed checks passed. Fork Actions require maintainer approval and Vercel requires external-contributor authorization.
- **Pipedream:** the sparse checkout omits 1,250 unrelated app sources, so global key/app-property validation cannot complete. Unmodified official validators passed in an isolated fixture linked to the real CompanyEnrich source; the global duplicate-key check also passed. [App registration](https://github.com/PipedreamHQ/pipedream/issues/22385) remains necessary before an upstream PR.
- **Dify:** the PR remains a draft pending real Dify deployment/remote-debugging validation. The [upstream package precheck](https://github.com/langgenius/dify-plugins/actions/runs/41191554571/job/124530143244) now passes on `15e1cb5`, including package contents, secret scan, manifest, dependencies, plugin installation and packaging. Earlier local warnings concerned the manifest's network-domain declaration, unpinned dependencies/offline vulnerability lookup, and a scanner heuristic that mistakes the HTTP dispatcher's `execute` name for possible SQL. There is no database execution in that dispatcher. No blocking package findings remain.
- **Haystack:** live validation and publishing the prepared CI files remain outstanding. Proposal acceptance is not an explicit prerequisite for opening a PR; our earlier wording overstated that policy. Workflow files were not pushed because the credential lacks workflow scope; the [inert CI patch](haystack/upstream-ci.patch) remains review material, not active CI. The existing two live smoke tests only cover domain enrichment. No upstream PR is open.
- **Botpress:** the review PR has merged into the contributor fork. Upstream submission remains outstanding; the earlier upstream PR-creation attempt was denied, and the current search found no CompanyEnrich PR in `botpress/botpress`.
- **CrewAI:** the review-found error-handling issue is fixed in `bef3344a`; Bugbot, Cursor security and the linked-issue check now pass. Remote test/type/lint workflows still require maintainer authorization, and the maintainer's AI-contribution label remains required. Local checks listed above passed; a full local monorepo suite is not claimed.
- **Langflow:** the current `ef3a1dd8` snapshot has 223 successful checks, 12 skipped and 12 failed. The failures are Python 3.15 jobs outside CompanyEnrich: [backend tests](https://github.com/langflow-ai/langflow/actions/runs/41192240584/job/124511873369) show Toolguard/LiteLLM's removed `sre_constants` import, unsupported MarkItDown and a pandas worker crash; [Valkey](https://github.com/langflow-ai/langflow/actions/runs/41192240448/job/124511304924) cannot import `glide_shared.protobuf`. The performance check fails after incomplete backend shards; Docker now passes. These are log-based findings, not a fresh full-suite reproduction on the base branch. The provider's local 291 tests and package checks passed; no CompanyEnrich defect was identified in these failures.

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
