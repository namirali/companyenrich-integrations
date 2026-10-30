# CompanyEnrich for Klavis: integration assessment

Klavis accepts complete MCP server implementations under `mcp_servers/<provider>/`, rather than simple hosted endpoint listings. CompanyEnrich already provides a hosted MCP server, so clients that support remote servers can connect directly to `https://mcp.companyenrich.com/mcp` using `Authorization: Bearer <API_KEY>` as documented in the [official setup guide](https://docs.companyenrich.com/docs/mcp-server).

No CompanyEnrich implementation or pull request was found in Klavis on 2026-10-31. A native Klavis contribution would need:

- A server with company enrichment, company search and similar-company tools, using the documented CompanyEnrich REST APIs.
- Per-request credential isolation using Klavis's `x-auth-data` conventions; never expose the API key as a tool argument.
- Streamable HTTP serving, a Dockerfile and requirements, plus mocked tests covering authentication, input boundaries, request mapping, transport behavior and errors.
- Documentation that these calls consume CompanyEnrich credits and that result limits affect spend.
- The contributor's CLA signature.
- A successful natural-language client test for every tool, captured as a video or multiple screenshots showing the prompt, invoked tool, arguments and result.

The last item is explicitly required by the [MCP Server Guide](https://github.com/Klavis-AI/klavis/blob/main/MCP_SERVER_GUIDE.md#step-2-test-with-natural-language-and-document-it). It was not performed because no CompanyEnrich credential or billable API test was authorized for this assessment. A native server was not submitted as a finished integration without that evidence.

Relevant patterns: [Exa server](https://github.com/Klavis-AI/klavis/tree/main/mcp_servers/exa), [Tavily server](https://github.com/Klavis-AI/klavis/tree/main/mcp_servers/tavily), [contribution guide](https://github.com/Klavis-AI/klavis/blob/main/CONTRIBUTING.md).
