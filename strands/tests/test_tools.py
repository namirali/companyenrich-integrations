import httpx

from companyenrich_strands import CompanyEnrichTools


def test_framework_tools_and_dispatch(respx_mock):
    toolkit = CompanyEnrichTools(api_key="test-key")
    tools = toolkit.tools
    assert [tool.tool_name for tool in tools] == [
        "companyenrich_enrich_company",
        "companyenrich_search_companies",
        "companyenrich_similar_companies",
        "companyenrich_search_people",
        "companyenrich_lookup_person",
        "companyenrich_company_workforce",
        "companyenrich_enrich_company_by_properties",
        "companyenrich_enrich_companies_batch",
        "companyenrich_get_company",
        "companyenrich_get_person",
        "companyenrich_count_companies",
        "companyenrich_count_similar_companies",
        "companyenrich_advanced_operation",
    ]
    for tool in tools:
        schema = tool.tool_spec["inputSchema"]["json"]
        assert "api_key" not in schema["properties"]
        assert "self" not in schema["properties"]
    route = respx_mock.get("https://api.companyenrich.com/companies/enrich").mock(
        return_value=httpx.Response(200, json={"domain": "example.com"})
    )
    assert toolkit.companyenrich_enrich_company(domain="example.com") == {"domain": "example.com"}
    assert route.call_count == 1
