# CompanyEnrich for Dify

CompanyEnrich provides company and professional data through an API. This plugin brings company research, enrichment and people discovery into Dify workflows and agents.

The twelve core capabilities are domain enrichment, company search, lookalikes, people search, email-to-person lookup, workforce, company enrichment by name/social properties, batch enrichment (1–50 domains), company/person ID lookups, and company/lookalike counts. An explicit advanced selector exposes 42 documented operations in total, including those twelve. See [the operation list](https://github.com/namirali/companyenrich-integrations/blob/main/ADVANCED_OPERATIONS.md).

Search accepts structured filters and literal/semantic company queries. Dedicated inputs take precedence over fields in the filters object. Lookalikes accept 1–10 seeds. Supported expansion options include company workforce and people education; the API decides entitlements and credit costs. Full response fields, nested data, pagination metadata and scores are preserved.

Each invocation makes one request with no automatic retry, pagination, polling, or result-URL download. Advanced export jobs require an explicit count of 1–50,000. The documented schema allows a larger export count than the prose; this adapter uses the conservative 50,000 limit. Page-based search defaults to page 1 and size 10, with size at most 100 and a 10,000-result ceiling. Beta email operations require explicit `allow_beta=true`. The selector fixes the API host and operation mapping; it cannot call arbitrary URLs. Saved-list administration is deliberately outside this integration scope. `/me` is credential-validation-only and its response is never exposed.


## Setup

1. Install the CompanyEnrich plugin package in Dify (1.6.0 or later).
2. Create an API key in the [CompanyEnrich dashboard](https://app.companyenrich.com/).
3. Configure the provider with the key, without a `Bearer` prefix. Credential validation calls the free `GET /me` endpoint.
4. Add a CompanyEnrich tool to a workflow or agent. For search, try `B2B software companies in Germany`; for enrichment, provide `stripe.com`.

Tools preserve the complete CompanyEnrich JSON response. Objects are returned directly; array and number responses use `{ "data": ... }` because Dify JSON messages require an object. Counts preserve zero. Filters, matching properties and advanced body/query/path parameters are entered as JSON objects; domain and expansion lists use comma-separated text. Person IDs use decimal strings. Search and similar-company tools return exactly one page. `page_size` defaults to 10, supports 1–100, and `page × page_size` must be at most 10,000. Use explicit subsequent calls for more results.

Enrichment and discovery can consume CompanyEnrich credits. The plugin performs no automatic pagination or retries. A missing domain can return HTTP 404 while enrichment is queued by CompanyEnrich; consult the API documentation before retrying. API errors include only a status and safe guidance, not response bodies or credentials.

## Development

Use Python 3.12. Install `requirements-dev.txt`, run `python -m pytest -q` and `ruff check .`, then package the runtime files using the official Dify CLI: `dify plugin package <runtime-directory> -o companyenrich-0.1.0.difypkg`. Exclude tests, caches, development requirements, and virtual environments from the package.

The automated suite has 104 passing tests with Python 3.12 and `dify_plugin==0.9.1`. It covers all twelve core routes and all 42 advanced mappings through SDK tool invocation with mocked HTTP, plus provider credential validation, manifest loading, response preservation, beta opt-in, credit-related errors, pagination limits, and malformed responses.

On November 10, 2026, the submitted runtime was also tested with an authorized live CompanyEnrich API key through remote debugging on Dify Community Edition 1.19.0 and plugin daemon 0.6.14. All 13 tools registered. Credential validation and eleven core tools passed: domain enrichment, company search, people search, lookalikes, workforce, property-based enrichment, a single-domain batch, company/person ID lookups, and both count tools. The advanced selector passed a country lookup. Search tests requested one result per call, without expansions. The runtime checks consumed 22 credits; earlier direct SDK checks consumed 9 credits.

Live testing did not cover reverse-email lookup, the other advanced operations, bulk/export jobs, beta email, expansions, Dify Cloud, or execution through the workflow/agent UI. These limits do not replace the mocked route coverage above. No API keys or returned person/company records are included in the source, package, or test report.

[Source code](https://github.com/namirali/companyenrich-integrations/tree/main/dify) · [Support and contact](https://github.com/namirali/companyenrich-integrations/issues) · [API documentation](https://docs.companyenrich.com/) · [Privacy](PRIVACY.md)
