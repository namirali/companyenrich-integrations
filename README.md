# CompanyEnrich integrations

Adapters and connection examples for CompanyEnrich company enrichment, semantic company search, and lookalike discovery. Each directory documents its setup, validation, and upstream distribution status. See the [target-by-target assessment](TARGETS.md) for all upstream PRs, existing integrations, contribution prerequisites, and deferred targets.

## Available code

| Directory | Integration | Distribution |
| --- | --- | --- |
| [activepieces](activepieces) | Custom piece with three actions and credential validation | Standalone; upstream currently pauses external contributions |
| [corsair](corsair) | Company data plugin | Standalone; upstream claim and recorded validation required |
| [haystack](haystack) | Source branch link and pending CI patch | Live API tests and workflow permission required |
| [dify](dify) | Provider and three tools | Source for a Dify plugin package; deployment validation pending |
| [llama-index](llama-index) | Native tool specification | Standalone package; no new upstream integrations accepted |
| [strands](strands) | Native agent tools | Standalone package; no new upstream tools accepted |
| [camel](camel) | Toolkit prototype | Human review and accepted proposal required before upstream submission |
| [langchain](langchain) | Hosted MCP client example | Uses LangChain 1.4+ MCPAdapter |
| [mastra](mastra) | Hosted MCP client example | Uses the official CompanyEnrich MCP server |
| [windmill](windmill) | MCP resource template | Uses the official CompanyEnrich MCP server |
| [mcp-registry](mcp-registry) | Official registry manifest | Prepared; namespace ownership and registry publication pending |
| [mcp-directories](mcp-directories) | Directory submission metadata | Prepared; website submission and listing prerequisites pending |
| [klavis](klavis) | Integration assessment | Native server and live validation required; hosted MCP already available |

## API and testing

REST adapters use `https://api.companyenrich.com` and bearer API keys. MCP examples use `https://mcp.companyenrich.com/mcp`. Get a key from the [dashboard](https://app.companyenrich.com/) and consult the [API documentation](https://docs.companyenrich.com/).

Data requests can consume credits. Adapters default to small, explicit requests and document pagination. Mocked tests verify authentication, request schemas, response handling, and errors. No live authenticated or billable API calls were made while preparing these integrations. Packages have not been published to npm or PyPI, and source availability does not mean upstream or marketplace approval.

These integrations were prepared with AI assistance and checked against public API documentation and current framework interfaces. See each directory for exact validation and remaining prerequisites.

## Licensing

See each directory’s license and notice files where present. The root MIT license covers original code without a separate directory license; the Corsair adapter retains its Apache-2.0 license and attribution.
