# CompanyEnrich MCP Registry metadata

This is a prepared, unpublished registry manifest for the official hosted CompanyEnrich MCP server. It does not claim that this repository contains the server implementation. Version `1.0.0` identifies the initial metadata release.

The official registry does not accept listing pull requests. Publish from a CompanyEnrich-controlled project using `mcp-publisher` after proving control of the `com.companyenrich` namespace with the registry's DNS or HTTP verification flow. Do not publish this under that namespace without ownership verification.

Before publication:

1. Validate `server.json` with `mcp-publisher validate`.
2. Verify the current server tool list with an authorized CompanyEnrich API key.
3. Authenticate using the documented DNS or HTTP ownership flow for `companyenrich.com`.
4. Publish with `mcp-publisher publish` only when authorized to make the registry listing public.

Bearer authentication follows [CompanyEnrich's MCP setup guide](https://docs.companyenrich.com/docs/mcp-server). The five capabilities follow the [official AI agents page](https://companyenrich.com/solutions/ai-agents). Tool calls use CompanyEnrich credits. No API key belongs in this manifest.

On 2026-10-31, an unauthenticated `initialize` request returned HTTP 401 with a Bearer challenge. This confirms endpoint reachability, not a successful authenticated session. The public registry search returned no CompanyEnrich entries. No data tool was called.

Publishing instructions: [MCP registry quickstart](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx), [remote servers](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/remote-servers.mdx), and [namespace authentication](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/authentication.mdx).
