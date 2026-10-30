"""CompanyEnrich tools for Strands Agents."""

from strands import tool
from strands.types.tools import AgentTool

from ._client import CompanyEnrichClient


class CompanyEnrichTools(CompanyEnrichClient):
    """Three company-data tools backed by a user's CompanyEnrich API key."""

    companyenrich_enrich_company = tool(CompanyEnrichClient.companyenrich_enrich_company)
    companyenrich_search_companies = tool(CompanyEnrichClient.companyenrich_search_companies)
    companyenrich_similar_companies = tool(CompanyEnrichClient.companyenrich_similar_companies)

    @property
    def tools(self) -> list[AgentTool]:
        """Return the tool objects to pass to strands.Agent(tools=...)."""
        return [
            self.companyenrich_enrich_company,
            self.companyenrich_search_companies,
            self.companyenrich_similar_companies,
        ]


__all__ = ["CompanyEnrichTools"]
