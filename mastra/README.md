# CompanyEnrich MCP with Mastra

Use Node.js 22.13 or later, install `@mastra/mcp`, provide `COMPANYENRICH_API_KEY` through your environment or secret manager, then run `node list-tools.mjs`. This example connects and lists available tools without executing them. In an existing Mastra application, pass the result of `await client.listTools()` as the agent's `tools`.

The example uses the remote URL and `requestInit.headers` contract in [Mastra's current MCP guide](https://mastra.ai/docs/connections/mcp), with the Bearer header from [CompanyEnrich's setup guide](https://docs.companyenrich.com/docs/mcp-server). Keep the client alive for the duration of tool use and disconnect afterward. Use a separate client per user when credentials differ.

Actual data tool calls consume CompanyEnrich credits. On 2026-10-31, the example was tested with `@mastra/mcp` 2.7.0 against a local HTTP MCP fixture: authentication headers, initialization, tool discovery, and disconnect passed without invoking tools. A live authenticated CompanyEnrich connection was not run. Ensure the installed Mastra MCP version supports the protocol revision offered by the server.
