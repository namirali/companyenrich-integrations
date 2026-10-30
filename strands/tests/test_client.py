import json

import httpx
import pytest

from companyenrich_strands._client import CompanyEnrichClient


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("COMPANYENRICH_API_KEY", "test-environment-key")
    return CompanyEnrichClient(timeout=12)


@pytest.mark.parametrize(
    "method,path,kwargs,payload",
    [
        ("companyenrich_enrich_company", "/companies/enrich", {"domain": " example.com "}, None),
        (
            "companyenrich_search_companies",
            "/companies/search",
            {"semantic_query": "B2B SaaS", "page": 2, "page_size": 3},
            {"semanticQuery": "B2B SaaS", "page": 2, "pageSize": 3},
        ),
        (
            "companyenrich_similar_companies",
            "/companies/similar",
            {"domains": ["example.com"], "page": 2, "page_size": 3},
            {"domains": ["example.com"], "page": 2, "pageSize": 3},
        ),
    ],
)
@pytest.mark.parametrize("asynchronous", [False, True])
async def test_requests_and_responses(
    client, respx_mock, method, path, kwargs, payload, asynchronous
):
    response = {
        "items": [{"domain": "result.example"}],
        "page": 2,
        "totalPages": 7,
        "metadata": {"scores": {"id": 0.9}},
    }
    route = respx_mock.route(method="GET" if payload is None else "POST", path=path).mock(
        return_value=httpx.Response(200, json=response)
    )
    result = (
        await getattr(client, "a" + method)(**kwargs)
        if asynchronous
        else getattr(client, method)(**kwargs)
    )
    assert result == response
    assert route.call_count == 1
    request = route.calls[0].request
    assert request.url.host == "api.companyenrich.com"
    assert request.headers["authorization"] == "Bearer test-environment-key"
    assert request.extensions["timeout"]["read"] == 12
    if payload is None:
        assert request.url.params["domain"] == "example.com"
    else:
        assert json.loads(request.content) == payload


@pytest.mark.parametrize(
    "method,kwargs",
    [
        ("companyenrich_enrich_company", {"domain": " "}),
        ("companyenrich_search_companies", {"semantic_query": " "}),
        ("companyenrich_search_companies", {"semantic_query": "a" * 501}),
        ("companyenrich_search_companies", {"semantic_query": "software", "page": 0}),
        ("companyenrich_search_companies", {"semantic_query": "software", "page_size": 101}),
        (
            "companyenrich_search_companies",
            {"semantic_query": "software", "page": 101, "page_size": 100},
        ),
        ("companyenrich_similar_companies", {"domains": []}),
        ("companyenrich_similar_companies", {"domains": ["example.com"] * 11}),
        ("companyenrich_similar_companies", {"domains": [" "]}),
    ],
)
@pytest.mark.parametrize("asynchronous", [False, True])
async def test_invalid_inputs_never_call_api(client, respx_mock, method, kwargs, asynchronous):
    with pytest.raises(ValueError):
        if asynchronous:
            await getattr(client, "a" + method)(**kwargs)
        else:
            getattr(client, method)(**kwargs)
    assert len(respx_mock.calls) == 0


@pytest.mark.parametrize("status", [301, 401, 402, 429, 500])
@pytest.mark.parametrize("asynchronous", [False, True])
async def test_http_failures_are_not_retried(client, respx_mock, status, asynchronous):
    route = respx_mock.get("https://api.companyenrich.com/companies/enrich").mock(
        return_value=httpx.Response(status, headers={"location": "https://unexpected.example"})
    )
    with pytest.raises(httpx.HTTPStatusError):
        if asynchronous:
            await client.acompanyenrich_enrich_company("example.com")
        else:
            client.companyenrich_enrich_company("example.com")
    assert route.call_count == 1


@pytest.mark.parametrize("asynchronous", [False, True])
async def test_timeout(client, respx_mock, asynchronous):
    route = respx_mock.get("https://api.companyenrich.com/companies/enrich").mock(
        side_effect=httpx.ReadTimeout("timed out")
    )
    with pytest.raises(httpx.ReadTimeout):
        if asynchronous:
            await client.acompanyenrich_enrich_company("example.com")
        else:
            client.companyenrich_enrich_company("example.com")
    assert route.call_count == 1


def test_credential_precedence(monkeypatch, respx_mock):
    monkeypatch.setenv("COMPANYENRICH_API_KEY", "environment-key")
    client = CompanyEnrichClient(api_key="explicit-key")
    route = respx_mock.get("https://api.companyenrich.com/companies/enrich").mock(
        return_value=httpx.Response(200, json={"domain": "example.com"})
    )
    client.companyenrich_enrich_company("example.com")
    assert route.calls[0].request.headers["Authorization"] == "Bearer explicit-key"
    assert "explicit-key" not in repr(client)


def test_missing_key(monkeypatch):
    monkeypatch.delenv("COMPANYENRICH_API_KEY", raising=False)
    with pytest.raises(ValueError, match="COMPANYENRICH_API_KEY"):
        CompanyEnrichClient()


@pytest.mark.parametrize("timeout", [0, -1, float("nan"), float("inf")])
def test_invalid_timeout(timeout):
    with pytest.raises(ValueError, match="timeout"):
        CompanyEnrichClient(api_key="test-key", timeout=timeout)


def test_wrong_input_types(client, respx_mock):
    with pytest.raises(TypeError):
        client.companyenrich_similar_companies("example.com")
    with pytest.raises(TypeError):
        client.companyenrich_search_companies("software", page=True)
    assert len(respx_mock.calls) == 0


def test_non_object_response(client, respx_mock):
    respx_mock.get("https://api.companyenrich.com/companies/enrich").mock(
        return_value=httpx.Response(200, json=[])
    )
    with pytest.raises(ValueError, match="JSON object"):
        client.companyenrich_enrich_company("example.com")
