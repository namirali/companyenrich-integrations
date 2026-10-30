# CompanyEnrich MCP directory submissions

`submission.json` contains verified public metadata for the official hosted MCP server. It is preparation only; no directory listing, account, or paid review was created.

## wong2 / mcpservers.org

[wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) no longer accepts listing PRs. Use [the submission form](https://mcpservers.org/submit). It asks for the server name, category, short description, documentation URL, remote connection support, and contact email. Use the free plan. The category is a suggestion to map to the form's current choices. An owner must provide the contact email. Leave the optional registry name blank until the official registry entry is published.

## punkpeye

[awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers/blob/main/CONTRIBUTING.md) requires an installable public GitHub server repository. CompanyEnrich's official server is hosted, so the recommended destination is [awesome-remote-mcp-servers](https://github.com/punkpeye/awesome-remote-mcp-servers).

The remote list requires a live [Glama connector](https://glama.ai/mcp/connectors), its verified badge URL, and the submitting account to star the repository. Glama search returned no CompanyEnrich connector on 2026-10-31. Register and obtain the actual connector URL before opening a PR; do not invent a badge namespace. No star or connector registration was performed.

After the connector exists, insert the three-line entry alphabetically under Sales, using the real connector and badge URLs:

```markdown
- [CompanyEnrich](https://companyenrich.com/) `https://mcp.companyenrich.com/mcp`
  [![CompanyEnrich MCP connector](<VERIFIED_GLAMA_BADGE_URL>)](<VERIFIED_GLAMA_CONNECTOR_URL>)
  🔑 - Enrich company profiles, search companies and people, find lookalikes, and look up people by email.
```

The official documentation specifies an API key. The endpoint's unauthenticated challenge also advertises OAuth resource metadata, and the list's checker classifies Bearer challenges as OAuth. Do not claim a verified OAuth flow from that challenge alone; resolve the marker with maintainers or test the vendor's supported flow before submitting.

## Verification

- [Official connection and Bearer header](https://docs.companyenrich.com/docs/mcp-server)
- [Official capabilities and credit usage](https://companyenrich.com/solutions/ai-agents)
- Unauthenticated MCP `initialize`: HTTP 401, checked 2026-10-31; authenticated initialization and tool execution were not tested.
- `https://registry.modelcontextprotocol.io/v0.1/servers?search=companyenrich&limit=100` returned zero listings.
- No public CompanyEnrich MCP source repository was found in the official GitHub organization, so none is claimed.
