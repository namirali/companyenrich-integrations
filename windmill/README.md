# CompanyEnrich MCP with Windmill

Create a resource with type `mcp`, name it CompanyEnrich, and set the URL to `https://mcp.companyenrich.com/mcp`. Supply your CompanyEnrich API key in the resource's **Auth token** field. The example JSON shows the resource value shape; replace its placeholder through Windmill's secret controls, never commit a working key.

Add this MCP resource as a tool on an AI Agent step. Windmill discovers the server's tools. Select only the tools needed for the workflow using the MCP tool's include/exclude settings. Executing CompanyEnrich data tools consumes account credits.

The connection fields and discovery flow are documented in [Windmill's AI agent MCP tools guide](https://www.windmill.dev/docs/core_concepts/ai_agents#mcp-tools). The [MCP resource schema](https://hub.windmill.dev/integrations/mcp) defines `token` as an optional Bearer token. [CompanyEnrich's guide](https://docs.companyenrich.com/docs/mcp-server) confirms API key authentication.

This is a prepared configuration, not a published Windmill Hub integration. No resource was created and no authenticated tool call was made.
