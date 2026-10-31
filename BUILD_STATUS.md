# Integration build audit

Checked on 2026-10-31. This audit covers all 14 prepared native integrations and all five MCP examples or metadata artifacts. The remaining targets in [TARGETS.md](TARGETS.md) have no submitted implementation to build.

## Latest recheck — 2026-10-31 12:47 Europe/Istanbul

All prepared source branches and PR heads were rechecked. No new integration defect or actionable review finding was found, so no additional source fix was needed. All 15 fresh build, test, package-validation, and MCP runtime checks for the shared repository passed. Pipedream and Botpress also passed their fresh scoped checks. CrewAI, Haystack, and Langflow retain their previously validated, unchanged source commits; current remote checks and review findings were inspected.

AutoGPT still has 54 successful checks; its remaining statuses are Vercel authorization and the CLA. Nango’s official provider validator now also passes locally. Nango, Sim, and Dify fork workflows still await maintainer approval. Langflow’s repaired integration checks remain green; the same upstream Python 3.15 and Docker runner failures remain. Sim’s refreshed full typecheck was attempted but hit a 120-second limit without diagnostics, so it remains unverified.

## Repairs pushed

| Integration | Repair | Verification |
| --- | --- | --- |
| [AutoGPT PR #16447](https://github.com/Significant-Gravitas/AutoGPT/pull/16447) | Added the required provider icon ID and PNG. Merged upstream `dev`, which already fixes unrelated roster assertions. | 74 catalog tests and all 70 unchanged MCP logo assertions pass locally. Remote rerun has 54 successful checks; remaining Vercel authorization and contribution gates are external to the code. |
| [Dify PR #3576](https://github.com/langgenius/dify-plugins/pull/3576) | Added the Marketplace-required contact email and rebuilt the `.difypkg`. Source is in this repository. | 27 tests, Ruff, official packaging, and all 12 local Marketplace checks pass. The new remote precheck awaits maintainer approval. |
| [Langflow PR #16078](https://github.com/langflow-ai/langflow/pull/16078) | Added the provider to the release inventory, bumped the bundle version and matching lock metadata, added canonical migration targets, and corrected the filters input metadata. | Previously failing CI release scripts, release plan, SQLite application checks, and LFX tests on Python 3.11/3.14/3.15 are now green. Local provider tests: 38; migration tests: 163; release-script tests: 738 passed, 1 skipped. Wheel and sdist build pass. |
| [CrewAI PR #8844](https://github.com/crewAIInc/crewAI/pull/8844) | Exported all three tools from the namespace used for Studio catalog discovery. Added regression coverage through the real tool-spec extractor. | 34 tests, lint, formatting, wheel and sdist build pass. Posted checks pass or are neutral. |
| [Pipedream branch](https://github.com/namirali/pipedream/tree/codex/companyenrich-integration) | Added the missing workspace lockfile importer and renamed the helper test to the component validator's `common-` convention. | Frozen dependency install, build, component validators, and four tests pass. Hosted app registration still precedes an upstream PR. |

## Other implementations checked

| Integration | Result and limits |
| --- | --- |
| [Nango PR #8118](https://github.com/NangoHQ/nango/pull/8118) | The official provider validator passes locally with no CompanyEnrich warnings. Posted checks pass or are neutral. Twelve Actions workflows and the documentation preview require maintainer approval; those full builds have not run. No code repair identified. |
| [Sim draft PR #9485](https://github.com/simstudioai/sim/pull/9485) | Scoped lint, tests, and integration metadata checks pass. Vercel requires deployment authorization and Actions requires maintainer approval. A local full typecheck initially used stale Trigger.dev 4.7.6 dependencies. The pinned Bun 1.4.4 frozen install succeeded and now installs the committed 4.8.2 versions. A fresh full typecheck after the refresh hit a 120-second limit without diagnostics and remains unverified; scoped checks passed again and no source change was needed. |
| [Botpress fork PR #1](https://github.com/namirali/botpress/pull/1) | Botpress build, TypeScript, Botpress lint, and 11 tests pass. No posted CI checks. Upstream submission permission remains outstanding. |
| [Haystack source branch](https://github.com/namirali/haystack-core-integrations/tree/codex/companyenrich-integration) | Formatting, all source type checks, package build, and 35 tests pass; two live tests are skipped. No active fork CI. The proposed workflow remains an inert patch because the GitHub token cannot push workflow changes. |
| [Activepieces](activepieces) | TypeScript build and all 8 tests pass. |
| [Corsair](corsair) | TypeScript, ESM bundle and declaration builds, and all 8 tests pass. |
| [LlamaIndex](llama-index) | All 45 tests, wheel and sdist build pass. |
| [Strands](strands) | All 45 tests, wheel and sdist build pass. |
| [CAMEL](camel) | All 45 tests, wheel and sdist build pass. |

## MCP examples and metadata

| Artifact | Verification |
| --- | --- |
| [LangChain](langchain) | Example discovers tools through the actual `MCPAdapter` and an in-process FastMCP server. URL and bearer-token arguments checked. Tested with LangChain 1.4.7 and FastMCP 4.1.4. |
| [Mastra](mastra) | Actual example sends the bearer header, initializes, lists tools, and disconnects against a local HTTP MCP fixture. No tool calls. Tested with `@mastra/mcp` 2.7.0; documented its Node.js 22.13 minimum. |
| [Windmill](windmill) | Resource JSON parses and contains the documented server URL and a credential placeholder. No Windmill deployment performed. |
| [MCP Registry](mcp-registry) | Manifest passes the referenced official JSON schema. Namespace verification and registry publication remain outstanding. |
| [MCP directories](mcp-directories) | Submission metadata parses. Website listing and directory approval remain outstanding. |

## Remaining limits

Langflow's target branch still has Python 3.15 dependency incompatibilities outside CompanyEnrich: Toolguard imports LiteLLM code that requires the removed `sre_constants` module, and Valkey cannot import `glide_shared.protobuf`. The previous run also hit a pandas datetime worker crash and a deliberately unavailable MarkItDown dependency. The relevant dependency pins and code are unchanged by this integration. These failures were not hidden or bypassed.

Both attempts of Langflow's Docker job completed their build steps but were interrupted by runner shutdown while exporting image layers. No CompanyEnrich build error was reported in those logs; a successful image test still requires a completed runner execution.

Some remote checks remain running or require maintainer authorization; AutoGPT also requires the contributor CLA. A green local package check does not imply upstream acceptance. Dify remains a draft pending deployment testing; Haystack still needs its required live tests. No authenticated or credit-consuming CompanyEnrich requests were made during this audit, and no npm or PyPI packages were published.

Dify package SHA256: `f76659fcbb62f556db2ce88ea49d6a27c4ddc60a5edeba41c55a8a976052bcc5`.
