# CompanyEnrich MCP with LangChain

LangChain 1.4+ includes `MCPAdapter`. Connect to CompanyEnrich's existing hosted MCP server instead of adding a provider to LangChain core.

Install `requirements.txt`, set `COMPANYENRICH_API_KEY` securely in your environment (without `Bearer`), and run `python list_tools.py`. The example discovers tool definitions; it does not call company-data tools. Pass the returned tools to `create_agent` when ready to allow data operations, which may consume CompanyEnrich credits.

This example follows the current [LangChain MCP documentation](https://docs.langchain.com/oss/python/langchain/mcp) and [FastMCP bearer authentication guide](https://gofastmcp.com/clients/auth/bearer). The `langchain.mcp` interface is currently beta. On 2026-10-31, the example successfully discovered tools through the real `MCPAdapter` and an in-process FastMCP fixture, with the URL and bearer-token arguments checked. A live authenticated CompanyEnrich connection and agent execution have not been tested. This is a connection example, not an upstream PR or published provider package.
