# CompanyEnrich for Dify

Enrich a company by domain, search companies with a natural-language description, and find similar companies from one to ten seed domains.

## Setup

1. Install the CompanyEnrich plugin package in Dify (1.6.0 or later).
2. Create an API key in the [CompanyEnrich dashboard](https://app.companyenrich.com/).
3. Configure the provider with the key, without a `Bearer` prefix. Credential validation calls the free `GET /me` endpoint.
4. Add a CompanyEnrich tool to a workflow or agent. For search, try `B2B software companies in Germany`; for enrichment, provide `stripe.com`.

Tools return the original CompanyEnrich JSON object, including company fields and search pagination metadata. Search and similar-company tools return exactly one page. `page_size` defaults to 10, supports 1–100, and `page × page_size` must be at most 10,000. Use explicit subsequent calls for more results.

Enrichment and discovery can consume CompanyEnrich credits. The plugin performs no automatic pagination or retries. A missing domain can return HTTP 404 while enrichment is queued by CompanyEnrich; consult the API documentation before retrying. API errors include only a status and safe guidance, not response bodies or credentials.

## Development

Use Python 3.12. Install `requirements-dev.txt`, run `python -m pytest -q` and `ruff check .`, then package the runtime files using the official Dify CLI: `dify plugin package <runtime-directory> -o companyenrich-0.1.0.difypkg`. Exclude tests, caches, development requirements, and virtual environments from the package.

Validation covers mocked HTTP requests, SDK tool invocation, provider credential validation, manifest loading, credit-related errors, pagination limits, and malformed responses. Live account calls and a Dify Cloud/Community deployment have not been tested without a dedicated test account.

[Source code](https://github.com/namirali/companyenrich-integrations/tree/main/dify) · [Support and contact](https://github.com/namirali/companyenrich-integrations/issues) · [API documentation](https://docs.companyenrich.com/) · [Privacy](PRIVACY.md)
