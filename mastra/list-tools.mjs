import { MCPClient } from '@mastra/mcp';

const apiKey = process.env.COMPANYENRICH_API_KEY;
if (!apiKey) {
  throw new Error('Set COMPANYENRICH_API_KEY before connecting.');
}

const client = new MCPClient({
  id: 'companyenrich',
  servers: {
    companyenrich: {
      url: new URL('https://mcp.companyenrich.com/mcp'),
      requestInit: {
        headers: { Authorization: `Bearer ${apiKey}` },
      },
    },
  },
});

try {
  const tools = await client.listTools();
  console.log(Object.keys(tools));
} finally {
  await client.disconnect();
}
