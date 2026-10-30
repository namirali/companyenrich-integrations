# CompanyEnrich for Corsair

Standalone, unpublished CompanyEnrich plugin compatible with `corsair@0.1.153`. It provides validated company enrichment, paginated search and lookalike discovery, and a free credential check.

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

Enrichment costs 1 credit. Search costs 1 credit per returned company (1 minimum per request); similar-company discovery costs 5 per company (5 minimum). Neither the HTTP client nor plugin error handlers automatically retry requests. Rate-limit errors expose `retryAfter` from the provider for caller-controlled handling. Errors omit provider response bodies to avoid leaking account information.

The returned company projection includes id, name, domain, website, description, industry, employee/revenue ranges, founding year, and technologies. Null or missing values remain unknown. It does not request extra-cost workforce expansions.

Company snapshots are disabled by default. With a configured Corsair database, `companyenrich({ persistCompanies: true })` upserts returned profiles by provider UUID into the plugin's `companies` entity and records `refreshedAt`. This stores the latest projection, including nulls. A persistence failure propagates after the provider call; retrying that operation can spend credits again. Database persistence has not been exercised against a live database.

Official references: [enrichment](https://docs.companyenrich.com/reference/get_companies-enrich), [search](https://docs.companyenrich.com/reference/post_companies-search), [similar companies](https://docs.companyenrich.com/reference/post_companies-similar), [credential check](https://docs.companyenrich.com/reference/get_me). Brand asset: [official SVG](https://companyenrich.com/companyenrich-solo-logo.svg).

[Upstream proposal #2014](https://github.com/corsairdev/corsair/issues/2014) is open. Corsair requires an OSS claim and issue alignment before an upstream plugin PR, plus a working demo recording before merge. No claim, assignment, upstream PR, npm publication, live authenticated verification, or demo recording is asserted. The package remains private for review; upstream registration, generated docs, and package-manager wiring follow after the proposal is accepted.
