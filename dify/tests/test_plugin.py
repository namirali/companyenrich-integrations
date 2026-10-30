import json
from pathlib import Path

import pytest
import requests
import responses
import yaml
from dify_plugin.core.entities.plugin.setup import PluginConfiguration
from dify_plugin.entities.tool import ToolProviderConfiguration
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from common.client import CompanyEnrichClient, CompanyEnrichError
from provider.companyenrich import CompanyEnrichProvider
from tools.enrich_company import EnrichCompanyTool
from tools.find_similar_companies import FindSimilarCompaniesTool
from tools.search_companies import SearchCompaniesTool

BASE = "https://api.companyenrich.com"


def test_manifest_and_provider_load_through_sdk():
    manifest = PluginConfiguration.model_validate(
        yaml.safe_load(Path("manifest.yaml").read_text())
    )
    provider = ToolProviderConfiguration.model_validate(
        yaml.safe_load(Path("provider/companyenrich.yaml").read_text())
    )
    assert manifest.meta.runner.version == "3.12"
    assert [tool.identity.name for tool in provider.tools] == [
        "enrich_company",
        "search_companies",
        "find_similar_companies",
    ]
    assert all(Path(tool.extra.python.source).exists() for tool in provider.tools)
    assert Path("_assets", manifest.icon).exists()


@responses.activate
def test_provider_checks_free_account_endpoint():
    responses.get(BASE + "/me", json={"credits": 100})
    CompanyEnrichProvider()._validate_credentials({"api_key": "test-key"})
    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers["Authorization"] == "Bearer test-key"


@responses.activate
def test_provider_error_is_sanitized():
    responses.get(BASE + "/me", status=401, body="secret upstream detail")
    with pytest.raises(
        ToolProviderCredentialValidationError, match="HTTP 401"
    ) as error:
        CompanyEnrichProvider()._validate_credentials({"api_key": "test-key"})
    assert "secret upstream" not in str(error.value)


@pytest.mark.parametrize(
    "cls,params,path,body",
    [
        (
            EnrichCompanyTool,
            {"domain": "stripe.com"},
            "/companies/enrich?domain=stripe.com",
            None,
        ),
        (
            SearchCompaniesTool,
            {"query": "B2B software"},
            "/companies/search",
            {"semanticQuery": "B2B software", "page": 1, "pageSize": 10},
        ),
        (
            FindSimilarCompaniesTool,
            {"domains": "stripe.com, adyen.com", "page": 2.0, "page_size": 5},
            "/companies/similar",
            {"domains": ["stripe.com", "adyen.com"], "page": 2, "pageSize": 5},
        ),
    ],
)
@responses.activate
def test_sdk_tool_dispatch(cls, params, path, body):
    payload = (
        {"id": "example", "domain": "stripe.com"}
        if body is None
        else {"items": [{"domain": "example.com"}], "totalCount": 12}
    )
    responses.add("GET" if body is None else "POST", BASE + path, json=payload)
    tool = cls.from_credentials({"api_key": "test-key"})
    messages = list(tool._invoke(params))
    assert len(messages) == 1
    assert messages[0].message.json_object == payload
    assert len(responses.calls) == 1
    if body is not None:
        assert json.loads(responses.calls[0].request.body) == body


@pytest.mark.parametrize(
    "page,size",
    [(0, 10), (1, 0), (1, 101), (101, 100), (1.5, 10), (True, 10), (float("nan"), 10)],
)
@responses.activate
def test_invalid_pagination_makes_no_request(page, size):
    with pytest.raises(CompanyEnrichError):
        CompanyEnrichClient("test-key").search_companies("software", page, size)
    assert len(responses.calls) == 0


@pytest.mark.parametrize("domains", ["", "a.com,", ",a.com", ",".join(["a.com"] * 11)])
@responses.activate
def test_invalid_seed_input_makes_no_request(domains):
    with pytest.raises(CompanyEnrichError):
        CompanyEnrichClient("test-key").find_similar_companies(domains)
    assert len(responses.calls) == 0


@pytest.mark.parametrize("status", [301, 401, 402, 404, 429, 500])
@responses.activate
def test_api_errors_do_not_retry_or_expose_response(status):
    responses.get(
        BASE + "/companies/enrich", status=status, body="secret upstream detail"
    )
    with pytest.raises(CompanyEnrichError, match=f"HTTP {status}") as error:
        CompanyEnrichClient("test-key").enrich_company("stripe.com")
    assert "secret upstream detail" not in str(error.value)
    assert len(responses.calls) == 1


@responses.activate
def test_network_error_is_sanitized():
    responses.get(BASE + "/me", body=requests.ConnectionError("Bearer test-key"))
    with pytest.raises(CompanyEnrichError, match="could not be reached") as error:
        CompanyEnrichClient("test-key").verify_credentials()
    assert "test-key" not in str(error.value)


@pytest.mark.parametrize("body", ["not JSON", "[]", "null"])
@responses.activate
def test_malformed_payload_is_rejected(body):
    responses.get(BASE + "/me", body=body)
    with pytest.raises(CompanyEnrichError):
        CompanyEnrichClient("test-key").verify_credentials()
