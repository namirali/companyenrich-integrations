# Advanced CompanyEnrich operations

The advanced selector exposes **42 fixed operations**, including the twelve core capabilities. Its inputs are `operation`, `body`, `query`, `path_parameters` and `allow_beta` (some hosts label JSON query input `query_parameters`). The host and HTTP method are fixed by the selector. Required fields and bounds are checked before HTTP. Unknown query/path fields are rejected; additional JSON filter fields are preserved for server validation.

Email operations labeled Beta require explicit opt-in. Export creation requires an explicit count no greater than 50,000, following the conservative public prose limit where the schema disagrees. Job results/status URLs are returned as data. Calls never poll, retry, paginate, or follow result URLs automatically. Saved-list administration (five routes) and credential-only `GET /me` are excluded from the public selector. No undocumented job-posting or advertising routes are invented.

Source: current public API reference, audited 2026-10-31. The complete 48-operation inventory is [api-endpoints.json](api-endpoints.json).

| Operation key | Method / path | Reference |
| --- | --- | --- |
| `get_companies_enrich` | `GET /companies/enrich` | [Enrich by domain](https://docs.companyenrich.com/reference/get_companies-enrich) |
| `post_companies_enrich` | `POST /companies/enrich` | [Enrich by properties](https://docs.companyenrich.com/reference/post_companies-enrich) |
| `post_companies_enrich_batch` | `POST /companies/enrich/batch` | [Batch enrich](https://docs.companyenrich.com/reference/post_companies-enrich-batch) |
| `get_companies_workforce` | `GET /companies/workforce` | [Workforce](https://docs.companyenrich.com/reference/get_companies-workforce) |
| `get_companies_autocomplete` | `GET /companies/autocomplete` | [Autocomplete](https://docs.companyenrich.com/reference/get_companies-autocomplete) |
| `post_companies_enrich_bulk` | `POST /companies/enrich/bulk` | [Create job](https://docs.companyenrich.com/reference/post_companies-enrich-bulk) |
| `get_companies_enrich_bulk_jobid` | `GET /companies/enrich/bulk/{jobId}` | [Get job status](https://docs.companyenrich.com/reference/get_companies-enrich-bulk-jobid) |
| `get_companies_enrich_bulk_jobs` | `GET /companies/enrich/bulk/jobs` | [List jobs](https://docs.companyenrich.com/reference/get_companies-enrich-bulk-jobs) |
| `post_companies_search` | `POST /companies/search` | [Search](https://docs.companyenrich.com/reference/post_companies-search) |
| `post_companies_search_preview` | `POST /companies/search/preview` | [Preview](https://docs.companyenrich.com/reference/post_companies-search-preview) |
| `post_companies_search_count` | `POST /companies/search/count` | [Count](https://docs.companyenrich.com/reference/post_companies-search-count) |
| `post_companies_search_scroll` | `POST /companies/search/scroll` | [Scroll](https://docs.companyenrich.com/reference/post_companies-search-scroll) |
| `get_companies` | `GET /companies` | [Get by ID](https://docs.companyenrich.com/reference/get_companies) |
| `post_companies_search_async` | `POST /companies/search/async` | [Create export job](https://docs.companyenrich.com/reference/post_companies-search-async) |
| `get_companies_search_async_jobid` | `GET /companies/search/async/{jobId}` | [Get export job status](https://docs.companyenrich.com/reference/get_companies-search-async-jobid) |
| `get_companies_search_async_jobs` | `GET /companies/search/async/jobs` | [List export jobs](https://docs.companyenrich.com/reference/get_companies-search-async-jobs) |
| `post_companies_similar` | `POST /companies/similar` | [Find similar](https://docs.companyenrich.com/reference/post_companies-similar) |
| `post_companies_similar_preview` | `POST /companies/similar/preview` | [Preview](https://docs.companyenrich.com/reference/post_companies-similar-preview) |
| `post_companies_similar_count` | `POST /companies/similar/count` | [Count](https://docs.companyenrich.com/reference/post_companies-similar-count) |
| `post_companies_similar_scroll` | `POST /companies/similar/scroll` | [Scroll](https://docs.companyenrich.com/reference/post_companies-similar-scroll) |
| `post_people_lookup` | `POST /people/lookup` | [Lookup person](https://docs.companyenrich.com/reference/post_people-lookup) |
| `get_people` | `GET /people` | [Get by ID](https://docs.companyenrich.com/reference/get_people) |
| `post_people_search` | `POST /people/search` | [Search](https://docs.companyenrich.com/reference/post_people-search) |
| `post_people_search_scroll` | `POST /people/search/scroll` | [Scroll](https://docs.companyenrich.com/reference/post_people-search-scroll) |
| `get_people_email` **Beta** | `GET /people/email` | [Email (BETA)](https://docs.companyenrich.com/reference/get_people-email) |
| `post_people_email_bulk` **Beta** | `POST /people/email/bulk` | [Create bulk email enrichment job (BETA)](https://docs.companyenrich.com/reference/post_people-email-bulk) |
| `get_people_email_bulk_jobid` **Beta** | `GET /people/email/bulk/{jobId}` | [Get bulk email enrichment job status (BETA)](https://docs.companyenrich.com/reference/get_people-email-bulk-jobid) |
| `get_people_education` | `GET /people/education` | [Education](https://docs.companyenrich.com/reference/get_people-education) |
| `post_people_search_async` | `POST /people/search/async` | [Create export job](https://docs.companyenrich.com/reference/post_people-search-async) |
| `get_people_search_async_jobid` | `GET /people/search/async/{jobId}` | [Get export job status](https://docs.companyenrich.com/reference/get_people-search-async-jobid) |
| `get_people_search_async_jobs` | `GET /people/search/async/jobs` | [List export jobs](https://docs.companyenrich.com/reference/get_people-search-async-jobs) |
| `get_jobs` | `GET /jobs` | [List all jobs](https://docs.companyenrich.com/reference/get_jobs) |
| `get_jobs_jobid` | `GET /jobs/{jobId}` | [Get job details](https://docs.companyenrich.com/reference/get_jobs-jobid) |
| `get_geo_regions` | `GET /geo/regions` | [Get regions](https://docs.companyenrich.com/reference/get_geo-regions) |
| `get_geo_countries_countrycode` | `GET /geo/countries/{countryCode}` | [Get country by code](https://docs.companyenrich.com/reference/get_geo-countries-countrycode) |
| `post_geo_countries` | `POST /geo/countries` | [Search countries](https://docs.companyenrich.com/reference/post_geo-countries) |
| `post_geo_states` | `POST /geo/states` | [Search states](https://docs.companyenrich.com/reference/post_geo-states) |
| `post_geo_cities` | `POST /geo/cities` | [Search cities](https://docs.companyenrich.com/reference/post_geo-cities) |
| `get_industries` | `GET /industries` | [List industries](https://docs.companyenrich.com/reference/get_industries) |
| `get_keywords_autocomplete` | `GET /keywords/autocomplete` | [Lookup keywords](https://docs.companyenrich.com/reference/get_keywords-autocomplete) |
| `get_technologies_autocomplete` | `GET /technologies/autocomplete` | [Lookup technologies](https://docs.companyenrich.com/reference/get_technologies-autocomplete) |
| `get_positions_autocomplete` | `GET /positions/autocomplete` | [Lookup positions](https://docs.companyenrich.com/reference/get_positions-autocomplete) |
