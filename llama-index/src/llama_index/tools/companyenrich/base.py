"""CompanyEnrich tool specification for LlamaIndex agents."""

from llama_index.core.tools.tool_spec.base import BaseToolSpec

from ._client import CompanyEnrichClient


class CompanyEnrichToolSpec(CompanyEnrichClient, BaseToolSpec):
    """Enrich domains, search companies, and discover lookalikes.

    Supports native synchronous and asynchronous execution. Set
    COMPANYENRICH_API_KEY or pass api_key to the constructor.
    """

    spec_functions = [
        ("companyenrich_enrich_company", "acompanyenrich_enrich_company"),
        ("companyenrich_search_companies", "acompanyenrich_search_companies"),
        ("companyenrich_similar_companies", "acompanyenrich_similar_companies"),
    ]
