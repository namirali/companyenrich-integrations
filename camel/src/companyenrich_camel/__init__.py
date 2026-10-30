"""CompanyEnrich company research toolkit for CAMEL."""

from camel.toolkits import BaseToolkit, FunctionTool

from ._client import CompanyEnrichClient


class CompanyEnrichToolkit(CompanyEnrichClient, BaseToolkit):
    r"""Company enrichment, semantic search, and similar-company discovery.

    Args:
        api_key (str, optional): API key, falling back to
            COMPANYENRICH_API_KEY.
        timeout (float): HTTP timeout in seconds. Defaults to 30.
    """

    def __init__(self, api_key: str | None = None, timeout: float = 30) -> None:
        BaseToolkit.__init__(self, timeout=timeout)
        CompanyEnrichClient.__init__(self, api_key=api_key, timeout=timeout)

    def get_tools(self) -> list[FunctionTool]:
        r"""Return the three company research tools.

        Returns:
            list[FunctionTool]: CompanyEnrich tools for ChatAgent.
        """
        return [
            FunctionTool(self.companyenrich_enrich_company),
            FunctionTool(self.companyenrich_search_companies),
            FunctionTool(self.companyenrich_similar_companies),
        ]


__all__ = ["CompanyEnrichToolkit"]
