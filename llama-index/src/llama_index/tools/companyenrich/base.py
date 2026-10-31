"""CompanyEnrich tool specification for LlamaIndex agents."""

from llama_index.core.tools.tool_spec.base import BaseToolSpec

from ._client import CompanyEnrichClient


class CompanyEnrichToolSpec(CompanyEnrichClient, BaseToolSpec):
    """Company and people tools with native synchronous and asynchronous execution."""

    spec_functions = [
        ("companyenrich_enrich_company", "acompanyenrich_enrich_company"),
        ("companyenrich_search_companies", "acompanyenrich_search_companies"),
        ("companyenrich_similar_companies", "acompanyenrich_similar_companies"),
        ("companyenrich_search_people", "acompanyenrich_search_people"),
        ("companyenrich_lookup_person", "acompanyenrich_lookup_person"),
        ("companyenrich_company_workforce", "acompanyenrich_company_workforce"),
        (
            "companyenrich_enrich_company_by_properties",
            "acompanyenrich_enrich_company_by_properties",
        ),
        ("companyenrich_enrich_companies_batch", "acompanyenrich_enrich_companies_batch"),
        ("companyenrich_get_company", "acompanyenrich_get_company"),
        ("companyenrich_get_person", "acompanyenrich_get_person"),
        ("companyenrich_count_companies", "acompanyenrich_count_companies"),
        ("companyenrich_count_similar_companies", "acompanyenrich_count_similar_companies"),
        ("companyenrich_advanced_operation", "acompanyenrich_advanced_operation"),
    ]
