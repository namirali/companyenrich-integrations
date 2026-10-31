import httpx

from llama_index.tools.companyenrich import CompanyEnrichToolSpec


async def test_framework_tools_and_async_dispatch(respx_mock):
    spec = CompanyEnrichToolSpec(api_key="test-key")
    tools = spec.to_tool_list()
    assert [tool.metadata.name for tool in tools] == [
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
        schema = tool.metadata.get_parameters_dict()
        assert "api_key" not in schema["properties"]
        assert "self" not in schema["properties"]
    route = respx_mock.get("https://api.companyenrich.com/companies/enrich").mock(
        return_value=httpx.Response(200, json={"domain": "example.com"})
    )
    assert tools[0].call(domain="example.com").raw_output == {"domain": "example.com"}
    assert (await tools[0].acall(domain="example.com")).raw_output == {"domain": "example.com"}
    assert route.call_count == 2
