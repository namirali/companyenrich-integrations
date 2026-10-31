import importlib
import json
from pathlib import Path

import pytest
import responses
from dify_plugin import Tool

from common.actions import OPERATIONS
from common.client import CompanyEnrichError

BASE = "https://api.companyenrich.com"


def invoke(name, params):
    module = importlib.import_module("tools." + name)
    cls = next(
        c
        for c in vars(module).values()
        if isinstance(c, type) and issubclass(c, Tool) and c is not Tool
    )
    return list(cls.from_credentials({"api_key": "test-key"})._invoke(params))[
        0
    ].message.json_object


CASES = [
    ("enrich_company", {"domain": "example.com"}, "GET", "/companies/enrich"),
    ("search_companies", {"query": "software"}, "POST", "/companies/search"),
    (
        "find_similar_companies",
        {"domains": "example.com"},
        "POST",
        "/companies/similar",
    ),
    ("search_people", {"query": "Sam"}, "POST", "/people/search"),
    ("lookup_person", {"email": "sam@example.com"}, "POST", "/people/lookup"),
    ("get_workforce", {"domain": "example.com"}, "GET", "/companies/workforce"),
    (
        "enrich_company_by_properties",
        {"properties": '{"name":"Example"}'},
        "POST",
        "/companies/enrich",
    ),
    (
        "enrich_companies_batch",
        {"domains": "example.com,example.org"},
        "POST",
        "/companies/enrich/batch",
    ),
    (
        "get_company",
        {"id": "550e8400-e29b-41d4-a716-446655440000"},
        "GET",
        "/companies",
    ),
    ("get_person", {"id": "9223372036854775807"}, "GET", "/people"),
    ("count_companies", {"query": "software"}, "POST", "/companies/search/count"),
    (
        "count_similar_companies",
        {"domains": "example.com"},
        "POST",
        "/companies/similar/count",
    ),
]


@pytest.mark.parametrize("name,params,method,path", CASES)
@responses.activate
def test_core_registered_tool_routes_and_preserves_response(name, params, method, path):
    payload = (
        0
        if name.startswith("count_")
        else [{"future": {"x": 1}}]
        if name == "enrich_companies_batch"
        else {"future": {"signals": [1]}, "metadata": {"scores": {"id": 0.9}}}
    )
    responses.add(method, BASE + path, json=payload)
    assert invoke(name, params) == (
        payload if isinstance(payload, dict) else {"data": payload}
    )
    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers["Authorization"] == "Bearer test-key"
    if name == "get_person":
        assert "9223372036854775807" in responses.calls[0].request.url


FIXTURES = json.loads(Path("tests/route-fixtures.json").read_text())


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda f: f["input"]["operation"])
@responses.activate
def test_advanced_routes(fixture):
    p = dict(fixture["input"])
    for key, target in [
        ("body", "body"),
        ("query", "query_parameters"),
        ("path_parameters", "path_parameters"),
    ]:
        if key in p:
            p[target] = json.dumps(p.pop(key))
    responses.add(fixture["method"], BASE + fixture["path"], json=0)
    assert invoke("advanced_operation", p) == {"data": 0}
    assert len(responses.calls) == 1


@responses.activate
def test_filters_expansions_and_seed_lists():
    responses.post(BASE + "/companies/similar", json={})
    invoke(
        "find_similar_companies",
        {
            "domains": "example.com, example.org",
            "filters": '{"countries":["US"],"future":{"x":true}}',
            "expand": "workforce",
            "wait_for_enrichment": False,
        },
    )
    request = responses.calls[0].request
    assert json.loads(request.body) == {
        "domains": ["example.com", "example.org"],
        "countries": ["US"],
        "future": {"x": True},
        "page": 1,
        "pageSize": 10,
    }
    assert (
        "expand=workforce" in request.url and "waitForEnrichment=false" in request.url
    )


@pytest.mark.parametrize(
    "p",
    [
        {"operation": "get_people_email", "query_parameters": '{"id":"42"}'},
        {"operation": "get_me"},
        {"operation": "get_companies_workforce"},
        {"operation": "post_companies_enrich_batch", "body": '{"domains":[]}'},
        {"operation": "post_companies_search", "body": '{"page":true}'},
        {"operation": "post_companies_search_async", "body": '{"count":50001}'},
        {"operation": "get_people", "query_parameters": '{"id":"9223372036854775808"}'},
        {
            "operation": "get_companies_enrich",
            "query_parameters": '{"domain":"example.com","host":"elsewhere"}',
        },
        {"operation": "post_companies_search", "body": "[]"},
    ],
)
@responses.activate
def test_invalid_inputs_make_no_request(p):
    with pytest.raises((CompanyEnrichError, ValueError)):
        invoke("advanced_operation", p)
    assert not responses.calls


@pytest.mark.parametrize("status", [301, 401, 402, 429, 500])
@responses.activate
def test_advanced_paid_failure_has_no_retry_or_secret_output(status):
    responses.post(
        BASE + "/companies/enrich/bulk",
        status=status,
        body="Authorization: Bearer private-secret",
    )
    with pytest.raises(CompanyEnrichError) as error:
        invoke(
            "advanced_operation",
            {
                "operation": "post_companies_enrich_bulk",
                "body": '{"domains":["example.com"]}',
            },
        )
    assert "private-secret" not in str(error.value)
    assert len(responses.calls) == 1


def test_public_core_inventory():
    assert {x[0] for x in CASES} == set(OPERATIONS)


@pytest.mark.parametrize(
    "body", [{"count": 1, "similar": {}}, {"count": 1, "similar": {"domains": [""]}}]
)
@responses.activate
def test_export_requires_valid_similar_seed_domains(body):
    with pytest.raises(CompanyEnrichError):
        invoke(
            "advanced_operation",
            {"operation": "post_companies_search_async", "body": json.dumps(body)},
        )
    assert not responses.calls


@responses.activate
def test_unknown_nested_nonfinite_number_rejected_before_http():
    with pytest.raises(CompanyEnrichError):
        invoke(
            "advanced_operation",
            {"operation": "post_companies_search", "body": '{"future":{"value":NaN}}'},
        )
    assert not responses.calls


@responses.activate
def test_scroll_default_is_bounded_and_cursor_not_followed():
    responses.post(BASE + "/people/search/scroll", json={"nextCursor": "next"})
    assert invoke("advanced_operation", {"operation": "post_people_search_scroll"}) == {
        "nextCursor": "next"
    }
    assert json.loads(responses.calls[0].request.body)["pageSize"] == 10
    assert len(responses.calls) == 1


@pytest.mark.parametrize(
    "name,params",
    [
        ("search_companies", {"query": "software", "page": True}),
        (
            "advanced_operation",
            {
                "operation": "get_people_email",
                "query_parameters": '{"id":"1"}',
                "allow_beta": "true",
            },
        ),
        (
            "advanced_operation",
            {
                "operation": "get_people_email",
                "query_parameters": '{"id":"1"}',
                "allow_beta": 1,
            },
        ),
    ],
)
@responses.activate
def test_public_sdk_invoke_rejects_type_coercion_before_network(name, params):
    module = importlib.import_module("tools." + name)
    cls = next(
        value
        for value in vars(module).values()
        if isinstance(value, type) and issubclass(value, Tool) and value is not Tool
    )
    with pytest.raises((CompanyEnrichError, ValueError)):
        list(cls.from_credentials({"api_key": "test-key"}).invoke(params))
    assert len(responses.calls) == 0
