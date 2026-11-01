# CompanyEnrich for Corsair

Standalone, unpublished CompanyEnrich plugin compatible with `corsair@0.1.153`. It provides twelve core data operations, a fixed advanced-operation selector, and a free credential check.

The twelve core capabilities are domain enrichment, company search, lookalikes, people search, email-to-person lookup, workforce, company enrichment by name/social properties, batch enrichment (1–50 domains), company/person ID lookups, and company/lookalike counts. An explicit advanced selector exposes 42 documented operations in total, including those twelve. See [the operation list](https://github.com/namirali/companyenrich-integrations/blob/main/ADVANCED_OPERATIONS.md).

Search accepts structured filters and literal/semantic company queries. Dedicated inputs take precedence over fields in the filters object. Lookalikes accept 1–10 seeds. Supported expansion options include company workforce and people education; the API decides entitlements and credit costs. Full response fields, nested data, pagination metadata and scores are preserved.

Each invocation makes one request with no automatic retry, pagination, polling, or result-URL download. Advanced export jobs require an explicit count of 1–50,000. The documented schema allows a larger export count than the prose; this adapter uses the conservative 50,000 limit. Page-based search defaults to page 1 and size 10, with size at most 100 and a 10,000-result ceiling. Beta email operations require explicit `allow_beta=true`. The selector fixes the API host and operation mapping; it cannot call arbitrary URLs. Saved-list administration is deliberately outside this integration scope. `/me` is credential-validation-only and its response is never exposed.


```sh
npm ci
npm run build
npm test
```

```typescript
import { createCorsair } from 'corsair/core';
import { companyenrich } from './index';

const client = createCorsair({
  plugins: [companyenrich({ key: process.env.COMPANYENRICH_API_KEY })],
});
await client.companyenrich.api.account.validate({});
const company = await client.companyenrich.api.companies.enrich({ domain: 'example.com' });
const page = await client.companyenrich.api.companies.search({ query: 'Example', page: 1, pageSize: 10 });
const lookalikes = await client.companyenrich.api.companies.similar({ domains: ['example.com'], pageSize: 10 });
```

Keys can also be supplied through Corsair's account key manager. Enter the key without the Bearer prefix. Obtain it from the [dashboard](https://app.companyenrich.com/). `account.validate` returns only `{ valid: true }`; the provider's `/me` response, including any account key, is discarded.

Search and similar-company discovery return one page per call. `page` is one-based; `pageSize` defaults to 10 and cannot exceed 100; `page * pageSize` cannot exceed 10,000. Explicitly request the next page using the returned totals. Similar-company responses preserve `metadata.scores`, keyed by company UUID.

Enrichment costs 1 credit. Search costs 1 credit per returned company (1 minimum per request); similar-company discovery costs 5 per company (5 minimum). Neither the HTTP client nor plugin error handlers automatically retry requests. Requests use a 30-second timeout with redirects disabled. Errors omit provider response bodies to avoid leaking account information.

Returned company and page objects preserve additional API fields. Request workforce expansions explicitly through `expand: ["workforce"]`; these can consume additional credits.

Company snapshots are disabled by default. With a configured Corsair database, `companyenrich({ persistCompanies: true })` upserts returned profiles by provider UUID into the plugin's `companies` entity and records `refreshedAt`. This stores the latest profile, including nulls. A persistence failure propagates after the provider call; retrying that operation can spend credits again. Database persistence has not been exercised against a live database.

Official references: [enrichment](https://docs.companyenrich.com/reference/get_companies-enrich), [search](https://docs.companyenrich.com/reference/post_companies-search), [similar companies](https://docs.companyenrich.com/reference/post_companies-similar), [credential check](https://docs.companyenrich.com/reference/get_me). Brand asset: [official SVG](https://companyenrich.com/companyenrich-solo-logo.svg).

[Upstream proposal #2014](https://github.com/corsairdev/corsair/issues/2014) is open. Corsair's contribution process calls for an OSS claim and issue alignment; waiting for maintainer assignment is recommended. Its plugin PR rules require a working demo recording before merge. No claim, assignment, upstream PR, npm publication, live authenticated verification, or demo recording is asserted. The package remains private for review; upstream registration, generated docs, and package-manager wiring remain to be completed.

## Expanded API

- `companies`: `enrich`, `search`, `similar`, `workforce`, `enrichByProperties`, `enrichBatch`, `get`, `count`, `similarCount`.
- `people`: `search`, `lookup`, `get`.
- `client.companyenrich.api.api.advanced({ operation, body?, query?, path_parameters?, allow_beta? })`.

For example, `client.companyenrich.api.people.search({ filters: { domains: ["example.com"] }, expand: ["education"] })` preserves all returned people fields. Pass large person IDs as decimal strings to avoid JavaScript precision loss. Counts return numbers (including zero); batch enrichment returns an array. Company persistence remains opt-in and applies to the company profile/page operations; the advanced selector does not persist results.
