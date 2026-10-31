"""Dify inputs for the fixed CompanyEnrich operation catalog."""

import json
from typing import Any

from common.client import CompanyEnrichClient, CompanyEnrichError
from common._validation import merge_filters

OPERATIONS = {
    "enrich_company": "get_companies_enrich",
    "search_companies": "post_companies_search",
    "find_similar_companies": "post_companies_similar",
    "search_people": "post_people_search",
    "lookup_person": "post_people_lookup",
    "get_workforce": "get_companies_workforce",
    "enrich_company_by_properties": "post_companies_enrich",
    "enrich_companies_batch": "post_companies_enrich_batch",
    "get_company": "get_companies",
    "get_person": "get_people",
    "count_companies": "post_companies_search_count",
    "count_similar_companies": "post_companies_similar_count",
}


def object_input(value: Any, name: str) -> dict:
    if value is None or value == "":
        return {}
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            raise CompanyEnrichError(f"{name} must be a JSON object.") from None
    if not isinstance(value, dict):
        raise CompanyEnrichError(f"{name} must be a JSON object.")
    return value


def values(value: Any, name: str) -> list:
    if not isinstance(value, str):
        raise CompanyEnrichError(f"{name} must be comma-separated text.")
    result = [part.strip() for part in value.split(",")]
    if any(not part for part in result):
        raise CompanyEnrichError(f"{name} must contain nonempty values.")
    return result


def invoke(name: str, p: dict[str, Any], api_key: str) -> Any:
    client = CompanyEnrichClient(api_key)
    if name == "advanced_operation":
        return client.execute(
            p.get("operation", ""),
            body=object_input(p.get("body"), "body"),
            query=object_input(p.get("query_parameters"), "query_parameters"),
            path_parameters=object_input(p.get("path_parameters"), "path_parameters"),
            allow_beta=p.get("allow_beta", False),
        )
    query, body = {}, None
    if p.get("expand"):
        query["expand"] = values(p["expand"], "expand")
    if "wait_for_enrichment" in p and p["wait_for_enrichment"] is not None:
        query["waitForEnrichment"] = p["wait_for_enrichment"]
    if name in {"enrich_company", "get_workforce", "get_company", "get_person"}:
        for key in ("id", "domain"):
            if p.get(key):
                query[key] = p[key]
    elif name == "enrich_company_by_properties":
        body = object_input(p.get("properties"), "properties")
    elif name == "enrich_companies_batch":
        body = {"domains": values(p.get("domains", ""), "domains")}
    elif name == "lookup_person":
        body = {"email": p.get("email", "")}
    else:
        dedicated = {}
        if name in {"search_companies", "count_companies"}:
            if p.get("query"):
                dedicated["semanticQuery"] = p["query"]
            if p.get("literal_query"):
                dedicated["query"] = p["literal_query"]
        if name == "search_people" and p.get("query"):
            dedicated["query"] = p["query"]
        if name in {"find_similar_companies", "count_similar_companies"}:
            dedicated["domains"] = values(p.get("domains", ""), "domains")
        if name in {"search_companies", "search_people", "find_similar_companies"}:
            page, size = client._pagination(p.get("page", 1), p.get("page_size", 10))
            dedicated.update(page=page, pageSize=size)
        body = merge_filters(object_input(p.get("filters"), "filters"), **dedicated)
    return client.execute(OPERATIONS[name], body=body, query=query)
