# CAMEL CompanyEnrich toolkit proposal draft

Status: requires human review and editing before submission. This AI-assisted prototype has not been submitted to CAMEL.

## Suggested issue title

CompanyEnrich toolkit for company enrichment, search, and lookalikes

## Draft

Would a CompanyEnrich toolkit be a useful addition to CAMEL? It would let agents enrich a company domain, search companies using a natural-language description, and find companies similar to one to ten seed domains.

I have prepared a standalone prototype with three namespaced FunctionTools, explicit API-key configuration, bounded pagination, no automatic retry of credit-consuming requests, and 45 mocked tests against CAMEL 0.2.90. Full API response metadata is preserved. The tests cover actual CAMEL schemas and dispatch as well as REST authentication, inputs, errors, and timeouts. No live authenticated API or LLM call has been made.

CompanyEnrich also offers a hosted MCP server, so using that may be preferable to maintaining an in-tree toolkit. The API reference is https://docs.companyenrich.com/reference and the MCP documentation is https://docs.companyenrich.com/docs/mcp-server.

This draft and code were prepared with AI assistance. Before submitting this proposal, a human must review and edit it. I would wait for an accepted discussion before preparing an upstream PR.

## Required next steps

1. Human review and editing of this proposal and prototype.
2. Submit the reviewed proposal and obtain explicit acceptance.
3. Human verification of tests; record evidence and make an authenticated smoke test only with authorized credentials/credits.
4. Adapt the accepted prototype to CAMEL's in-tree style and Apache-2.0 license, then submit a linked PR.

Policy: https://github.com/camel-ai/camel/blob/master/CONTRIBUTING.md#ai-generated-code-policy
