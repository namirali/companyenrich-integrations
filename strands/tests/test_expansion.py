import json
from pathlib import Path

import httpx
import pytest

from companyenrich_strands import CompanyEnrichTools
from companyenrich_strands._client import CompanyEnrichClient

CASES = json.loads(Path(__file__).with_name("operation_cases.json").read_text())
UUID = "123e4567-e89b-12d3-a456-426614174000"
RICH = {
    "items": [{"future": {"funding": [1, 2]}}],
    "page": 1,
    "metadata": {"scores": {"a": 0.8}},
    "future": [None, 0],
}
CORE = [
    ("companyenrich_enrich_company", "GET", "/companies/enrich", {"domain": "example.com"}, RICH),
    (
        "companyenrich_search_companies",
        "POST",
        "/companies/search",
        {"semantic_query": "software"},
        RICH,
    ),
    (
        "companyenrich_similar_companies",
        "POST",
        "/companies/similar",
        {"domains": ["example.com"]},
        RICH,
    ),
    ("companyenrich_search_people", "POST", "/people/search", {"filters": {"query": "Jane"}}, RICH),
    ("companyenrich_lookup_person", "POST", "/people/lookup", {"email": "jane@example.com"}, RICH),
    (
        "companyenrich_company_workforce",
        "GET",
        "/companies/workforce",
        {"domain": "example.com"},
        RICH,
    ),
    (
        "companyenrich_enrich_company_by_properties",
        "POST",
        "/companies/enrich",
        {"properties": {"name": "Example"}},
        RICH,
    ),
    (
        "companyenrich_enrich_companies_batch",
        "POST",
        "/companies/enrich/batch",
        {"domains": ["example.com"]},
        [RICH],
    ),
    ("companyenrich_get_company", "GET", "/companies", {"company_id": UUID}, RICH),
    ("companyenrich_get_person", "GET", "/people", {"person_id": "9223372036854775807"}, RICH),
    ("companyenrich_count_companies", "POST", "/companies/search/count", {"query": "software"}, 0),
    (
        "companyenrich_count_similar_companies",
        "POST",
        "/companies/similar/count",
        {"domains": ["example.com"]},
        0,
    ),
]


async def invoke(toolkit, name, kwargs, asynchronous):
    tools = {tool.tool_name: tool for tool in toolkit.tools}
    assert name in tools
    return await getattr(toolkit, "a" + name)(**kwargs) if asynchronous else tools[name](**kwargs)


def tool_schemas(toolkit):
    return {tool.tool_name: tool.tool_spec["inputSchema"]["json"] for tool in toolkit.tools}


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("name,method,path,kwargs,result", CORE)
async def test_core_tools_registered_and_dispatch(
    respx_mock, name, method, path, kwargs, result, asynchronous
):
    toolkit = CompanyEnrichTools(api_key="test-key")
    route = respx_mock.route(method=method, path=path).mock(
        return_value=httpx.Response(200, json=result)
    )
    assert await invoke(toolkit, name, kwargs, asynchronous) == result
    assert route.call_count == 1
    request = route.calls[0].request
    assert request.url.host == "api.companyenrich.com"
    assert request.headers["authorization"] == "Bearer test-key"
    if name == "companyenrich_get_person":
        assert request.url.params["id"] == "9223372036854775807"
    if name in {
        "companyenrich_search_companies",
        "companyenrich_similar_companies",
        "companyenrich_search_people",
    }:
        assert json.loads(request.content)["pageSize"] == 5


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("case", CASES, ids=lambda case: case["operation"])
async def test_all_advanced_routes_from_registered_tool(respx_mock, case, asynchronous):
    toolkit = CompanyEnrichTools(api_key="test-key")
    route = respx_mock.route(method=case["method"], path=case["path"]).mock(
        return_value=httpx.Response(200, json=case["result"])
    )
    kwargs = {
        key: case[key] for key in ("operation", "body", "query", "path_parameters", "allow_beta")
    }
    assert (
        await invoke(toolkit, "companyenrich_advanced_operation", kwargs, asynchronous)
        == case["result"]
    )
    assert route.call_count == 1
    assert route.calls[0].request.url.host == "api.companyenrich.com"


def test_framework_operation_enum_and_no_credential_inputs():
    toolkit = CompanyEnrichTools(api_key="secret")
    schemas = tool_schemas(toolkit)
    assert set(schemas) == {case[0] for case in CORE} | {"companyenrich_advanced_operation"}
    for schema in schemas.values():
        assert "api_key" not in schema["properties"]
        assert "self" not in schema["properties"]
    selector = json.dumps(schemas["companyenrich_advanced_operation"])
    for case in CASES:
        assert case["operation"] in selector
    assert "get_me" not in selector


@pytest.mark.parametrize("asynchronous", [False, True])
async def test_full_filters_expands_and_dedicated_precedence(respx_mock, asynchronous):
    toolkit = CompanyEnrichTools(api_key="test-key")
    route = respx_mock.post("https://api.companyenrich.com/companies/search").mock(
        return_value=httpx.Response(200, json=RICH)
    )
    filters = {
        "countries": ["US"],
        "technologies": ["React"],
        "exclude": {"domains": ["exclude.com"]},
        "future": {"deep": [None, True]},
        "semanticQuery": "old",
        "query": "old",
        "pageSize": 90,
    }
    result = await invoke(
        toolkit,
        "companyenrich_search_companies",
        {
            "semantic_query": "new semantic",
            "query": "literal",
            "filters": filters,
            "expand": ["workforce"],
        },
        asynchronous,
    )
    assert result == RICH
    assert json.loads(route.calls[0].request.content) == {
        **filters,
        "semanticQuery": "new semantic",
        "query": "literal",
        "page": 1,
        "pageSize": 5,
    }
    assert route.calls[0].request.url.params.get_list("expand") == ["workforce"]
    similar = respx_mock.post("https://api.companyenrich.com/companies/similar").mock(
        return_value=httpx.Response(200, json=RICH)
    )
    await invoke(
        toolkit,
        "companyenrich_similar_companies",
        {
            "domains": ["one.com", "two.com"],
            "filters": {"minScore": 0.5},
            "wait_for_enrichment": False,
            "expand": ["workforce"],
        },
        asynchronous,
    )
    assert json.loads(similar.calls[0].request.content)["minScore"] == 0.5
    assert similar.calls[0].request.url.params["waitForEnrichment"] == "false"


BAD = [
    {"operation": "get_me"},
    {"operation": "https://evil.example"},
    {"operation": "get_companies_enrich", "query": {"domain": " "}},
    {
        "operation": "get_companies_enrich",
        "query": {"domain": "example.com", "url": "https://evil.example"},
    },
    {
        "operation": "get_companies_enrich",
        "query": {"domain": "example.com", "expand": ["education"]},
    },
    {
        "operation": "get_companies_enrich",
        "query": {"domain": "example.com", "waitForEnrichment": "true"},
    },
    {"operation": "get_companies_workforce"},
    {"operation": "get_companies_workforce", "query": {"domain": "example.com", "id": UUID}},
    {"operation": "get_companies", "query": {"id": "invalid"}},
    {"operation": "get_people", "query": {"id": True}},
    {"operation": "get_people", "query": {"id": "9223372036854775808"}},
    {"operation": "post_companies_enrich", "body": {}},
    {"operation": "post_companies_enrich_batch", "body": {"domains": []}},
    {"operation": "post_companies_enrich_batch", "body": {"domains": ["example.com"] * 51}},
    {"operation": "post_companies_similar", "body": {"domains": ["example.com"] * 11}},
    {"operation": "post_companies_similar_count", "body": {"domain": "example.com"}},
    {"operation": "post_people_lookup", "body": {"email": " "}},
    {"operation": "post_companies_search", "body": {"page": True}},
    {"operation": "post_companies_search", "body": {"pageSize": 101}},
    {"operation": "post_companies_search", "body": {"page": 101, "pageSize": 100}},
    {"operation": "post_companies_search", "body": {"query": "x" * 251}},
    {"operation": "post_companies_search", "body": {"semanticQuery": "x" * 501}},
    {"operation": "post_companies_search", "body": []},
    {"operation": "post_companies_search", "body": {"future": float("nan")}},
    {"operation": "post_companies_search", "body": {"future": float("inf")}},
    {"operation": "post_companies_search", "body": {"future": {1: "bad"}}},
    {"operation": "post_companies_search_async", "body": {}},
    {"operation": "post_companies_search_async", "body": {"count": 50001}},
    {"operation": "post_companies_search_async", "body": {"count": 1, "similar": {}}},
    {
        "operation": "post_companies_search_async",
        "body": {"count": 1, "similar": {"domains": [""]}},
    },
    {"operation": "post_people_email_bulk", "body": {"items": []}, "allow_beta": True},
    {"operation": "post_people_email_bulk", "body": {"items": [{}]}, "allow_beta": True},
    {"operation": "get_geo_countries_countrycode", "path_parameters": {"countryCode": "."}},
    {"operation": "get_geo_countries_countrycode", "path_parameters": {"countryCode": ".."}},
    {"operation": "get_jobs_jobid", "path_parameters": {"jobId": UUID, "extra": "x"}},
    {"operation": "get_jobs_jobid"},
    {"operation": "get_jobs", "query": {"status": "nope"}},
    {"operation": "get_jobs", "body": {"query": "nope"}},
    {"operation": "get_jobs", "allow_beta": "true"},
]


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("kwargs", BAD)
async def test_advanced_invalid_inputs_before_network(respx_mock, kwargs, asynchronous):
    client = CompanyEnrichClient(api_key="test-key")
    with pytest.raises((ValueError, TypeError)):
        if asynchronous:
            await client.acompanyenrich_advanced_operation(**kwargs)
        else:
            client.companyenrich_advanced_operation(**kwargs)
    assert len(respx_mock.calls) == 0


@pytest.mark.parametrize(
    "case",
    [
        case
        for case in CASES
        if case["operation"]
        in {"get_people_email", "post_people_email_bulk", "get_people_email_bulk_jobid"}
    ],
    ids=lambda case: case["operation"],
)
@pytest.mark.parametrize("asynchronous", [False, True])
async def test_beta_requires_explicit_opt_in(respx_mock, case, asynchronous):
    toolkit = CompanyEnrichTools(api_key="test-key")
    kwargs = {key: case[key] for key in ("operation", "body", "query", "path_parameters")}
    with pytest.raises(ValueError, match="beta"):
        await invoke(toolkit, "companyenrich_advanced_operation", kwargs, asynchronous)
    assert len(respx_mock.calls) == 0


@pytest.mark.parametrize("asynchronous", [False, True])
async def test_large_person_id_body_and_returned_urls(respx_mock, asynchronous):
    toolkit = CompanyEnrichTools(api_key="test-key")
    output = {"jobId": UUID, "resultUrl": "https://other.example/file", "status": "pending"}
    route = respx_mock.post("https://api.companyenrich.com/people/email/bulk").mock(
        return_value=httpx.Response(200, json=output)
    )
    kwargs = {
        "operation": "post_people_email_bulk",
        "body": {"items": [{"person_id": "9223372036854775807"}]},
        "allow_beta": True,
    }
    assert await invoke(toolkit, "companyenrich_advanced_operation", kwargs, asynchronous) == output
    assert (
        json.loads(route.calls[0].request.content)["items"][0]["person_id"] == 9223372036854775807
    )
    assert len(respx_mock.calls) == 1


@pytest.mark.parametrize("asynchronous", [False, True])
async def test_errors_do_not_expose_credentials_or_upstream_body(respx_mock, asynchronous):
    toolkit = CompanyEnrichTools(api_key="sensitive-api-key")
    route = respx_mock.post("https://api.companyenrich.com/companies/search").mock(
        return_value=httpx.Response(
            429, text="sensitive upstream body", headers={"x-private": "secret"}
        )
    )
    with pytest.raises(httpx.HTTPStatusError) as caught:
        await invoke(
            toolkit,
            "companyenrich_search_companies",
            {"semantic_query": "sensitive query"},
            asynchronous,
        )
    error = caught.value
    assert "429" in str(error)
    assert "sensitive" not in str(error)
    assert "authorization" not in error.request.headers
    assert not error.response.content
    assert "x-private" not in error.response.headers
    assert route.call_count == 1
    route.mock(side_effect=httpx.ReadTimeout("Bearer sensitive-api-key"))
    with pytest.raises(httpx.ReadTimeout) as caught:
        await invoke(
            toolkit, "companyenrich_search_companies", {"semantic_query": "software"}, asynchronous
        )
    assert "sensitive" not in str(caught.value)
    assert route.call_count == 2


@pytest.mark.parametrize("asynchronous", [False, True])
async def test_advanced_scroll_defaults_to_ten_results(respx_mock, asynchronous):
    client = CompanyEnrichClient(api_key="test-key")
    route = respx_mock.post("https://api.companyenrich.com/people/search/scroll").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    kwargs = {"operation": "post_people_search_scroll", "body": {"cursor": "next"}}
    if asynchronous:
        await client.acompanyenrich_advanced_operation(**kwargs)
    else:
        client.companyenrich_advanced_operation(**kwargs)
    assert json.loads(route.calls[0].request.content) == {"cursor": "next", "pageSize": 10}


COERCION_INPUTS = [
    ("companyenrich_search_companies", {"page": True}),
    ("companyenrich_search_people", {"filters": {}, "page_size": True}),
    ("companyenrich_get_person", {"person_id": True}),
    ("companyenrich_enrich_company", {"domain": "example.com", "wait_for_enrichment": "false"}),
    (
        "companyenrich_advanced_operation",
        {"operation": "get_people_email", "query": {"id": "1"}, "allow_beta": "true"},
    ),
    (
        "companyenrich_advanced_operation",
        {"operation": "get_people_email", "query": {"id": "1"}, "allow_beta": 1},
    ),
]


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("name,kwargs", COERCION_INPUTS)
async def test_registered_tools_reject_coercion_before_network(
    respx_mock, name, kwargs, asynchronous
):
    toolkit = CompanyEnrichTools(api_key="test-key")
    respx_mock.route().mock(return_value=httpx.Response(200, json={}))
    with pytest.raises((ValueError, TypeError)):
        await invoke(toolkit, name, kwargs, asynchronous)
    assert len(respx_mock.calls) == 0


@pytest.mark.parametrize("name,kwargs", COERCION_INPUTS)
async def test_strands_agent_stream_rejects_coercion(respx_mock, name, kwargs):
    toolkit = CompanyEnrichTools(api_key="test-key")
    selected = {tool.tool_name: tool for tool in toolkit.tools}[name]
    respx_mock.route().mock(return_value=httpx.Response(200, json={}))
    events = [
        event
        async for event in selected.stream(
            {"toolUseId": "mock-call", "name": name, "input": kwargs}, {}
        )
    ]
    assert events[-1]["tool_result"]["status"] == "error"
    assert len(respx_mock.calls) == 0


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["operation"])
async def test_strands_agent_stream_all_advanced_operations(respx_mock, case):
    selected = {tool.tool_name: tool for tool in CompanyEnrichTools(api_key="test-key").tools}[
        "companyenrich_advanced_operation"
    ]
    route = respx_mock.route(method=case["method"], path=case["path"]).mock(
        return_value=httpx.Response(200, json=case["result"])
    )
    kwargs = {
        key: case[key] for key in ("operation", "body", "query", "path_parameters", "allow_beta")
    }
    events = [
        event
        async for event in selected.stream(
            {"toolUseId": "mock-call", "name": selected.tool_name, "input": kwargs}, {}
        )
    ]
    assert events[-1]["tool_result"]["status"] == "success"
    assert json.loads(events[-1]["tool_result"]["content"][0]["text"]) == case["result"]
    assert route.call_count == 1


@pytest.mark.parametrize("name,method,path,kwargs,result", CORE)
async def test_strands_agent_stream_all_core_operations(
    respx_mock, name, method, path, kwargs, result
):
    selected = {tool.tool_name: tool for tool in CompanyEnrichTools(api_key="test-key").tools}[name]
    route = respx_mock.route(method=method, path=path).mock(
        return_value=httpx.Response(200, json=result)
    )
    events = [
        event
        async for event in selected.stream(
            {"toolUseId": "mock-call", "name": name, "input": kwargs}, {}
        )
    ]
    assert events[-1]["tool_result"]["status"] == "success"
    assert json.loads(events[-1]["tool_result"]["content"][0]["text"]) == result
    assert route.call_count == 1
