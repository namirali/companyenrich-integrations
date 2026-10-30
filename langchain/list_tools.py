"""Discover CompanyEnrich MCP tools; does not invoke paid data operations."""

import asyncio
import os

from fastmcp import Client
from langchain.mcp import MCPAdapter


async def main() -> None:
    api_key = os.environ.get("COMPANYENRICH_API_KEY", "").strip()
    if not api_key:
        raise ValueError("Set COMPANYENRICH_API_KEY before connecting.")
    client = Client("https://mcp.companyenrich.com/mcp", auth=api_key)
    async with MCPAdapter(client) as adapter:
        tools = await adapter.list_tools()
        print([tool.name for tool in tools])
        # Pass these tools to langchain.agents.create_agent when you are ready
        # to allow data operations, which can consume CompanyEnrich credits.


if __name__ == "__main__":
    asyncio.run(main())
