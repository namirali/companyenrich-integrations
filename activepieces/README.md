# CompanyEnrich for Activepieces

Standalone, unpublished piece source with twelve named actions plus Advanced API Operation. It targets the published Activepieces SDK (`pieces-framework` 0.32.0).

The twelve core capabilities are domain enrichment, company search, lookalikes, people search, email-to-person lookup, workforce, company enrichment by name/social properties, batch enrichment (1–50 domains), company/person ID lookups, and company/lookalike counts. An explicit advanced selector exposes 42 documented operations in total, including those twelve. See [the operation list](https://github.com/namirali/companyenrich-integrations/blob/main/ADVANCED_OPERATIONS.md).

Search accepts structured filters and literal/semantic company queries. Dedicated inputs take precedence over fields in the filters object. Lookalikes accept 1–10 seeds. Supported expansion options include company workforce and people education; the API decides entitlements and credit costs. Full response fields, nested data, pagination metadata and scores are preserved.

Each invocation makes one request with no automatic retry, pagination, polling, or result-URL download. Advanced export jobs require an explicit count of 1–50,000. The documented schema allows a larger export count than the prose; this adapter uses the conservative 50,000 limit. Page-based search defaults to page 1 and size 10, with size at most 100 and a 10,000-result ceiling. Beta email operations require explicit `allow_beta=true`. The selector fixes the API host and operation mapping; it cannot call arbitrary URLs. Saved-list administration is deliberately outside this integration scope. `/me` is credential-validation-only and its response is never exposed.

The API key is stored as a Secret Text connection and checked with the free `GET /me` endpoint. Obtain it from the [CompanyEnrich dashboard](https://app.companyenrich.com/) and omit the `Bearer` prefix.

```sh
npm ci
npm run build
npm test
```

Search and similar-company actions return one page, including `items`, `page`, `totalPages`, and `totalItems`. Use the Page input for subsequent pages. Page Size defaults to 10 and is bounded to 100. `page * pageSize` cannot exceed 10,000. Similar-company responses also retain match scores in `metadata.scores`.

Enrichment costs 1 credit per call. Search costs 1 credit per returned company (1 minimum per request); similar-company discovery costs 5 per company (5 minimum). No automatic retry is added to paid requests. Requests use native Node.js 18+ fetch with certificate verification, a 30-second timeout and redirects disabled. Errors report sanitized HTTP status or transport failure; provider error bodies are never exposed. Search query length is limited to 250 characters.

Official API references: [enrich](https://docs.companyenrich.com/reference/get_companies-enrich), [search](https://docs.companyenrich.com/reference/post_companies-search), [similar](https://docs.companyenrich.com/reference/post_companies-similar), [authentication check](https://docs.companyenrich.com/reference/get_me). The piece uses the official hosted CompanyEnrich SVG.

The current [Activepieces contribution policy](https://github.com/activepieces/activepieces/blob/main/CONTRIBUTING.md) pauses unsolicited external PRs. No upstream PR, npm publication, marketplace submission, or live authenticated execution was performed. The package is deliberately private. An owner can review and follow Activepieces' custom-piece publishing/import procedure once ready; availability depends on their Activepieces deployment and plan.
