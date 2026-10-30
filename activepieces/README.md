# CompanyEnrich for Activepieces

Standalone, unpublished piece source with three actions: enrich a company by domain, search company names/domains, and find similar companies from a seed domain. It targets the published Activepieces SDK (`pieces-framework` 0.32.0), rather than unpublished monorepo changes.

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
