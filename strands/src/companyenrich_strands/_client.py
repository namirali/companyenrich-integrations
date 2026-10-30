"""Bounded CompanyEnrich REST requests shared by the framework tools."""

import math
import os
from typing import Any

import httpx


def _text(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")
    return value.strip()


def _page(page: int, page_size: int) -> dict[str, int]:
    if type(page) is not int or type(page_size) is not int:
        raise TypeError("page and page_size must be integers")
    if page < 1 or not 1 <= page_size <= 100:
        raise ValueError("page must be positive and page_size must be between 1 and 100")
    return {"page": page, "pageSize": page_size}


def _search_payload(semantic_query: str, page: int, page_size: int) -> dict[str, Any]:
    payload: dict[str, Any] = _page(page, page_size)
    if page * page_size > 10000:
        raise ValueError("Company search requires page * page_size <= 10000")
    query = _text(semantic_query, "semantic_query")
    if len(query) > 500:
        raise ValueError("semantic_query must not exceed 500 characters")
    payload["semanticQuery"] = query
    return payload


def _similar_payload(domains: list[str], page: int, page_size: int) -> dict[str, Any]:
    if not isinstance(domains, list):
        raise TypeError("domains must be a list of strings")
    if not 1 <= len(domains) <= 10:
        raise ValueError("Provide one to ten seed domains")
    return {**_page(page, page_size), "domains": [_text(domain, "domain") for domain in domains]}


def _result(response: httpx.Response) -> dict[str, Any]:
    response.raise_for_status()
    result = response.json()
    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object from CompanyEnrich")
    return result


class CompanyEnrichClient:
    """REST client with one request per method and no automatic paid retries.

    Args:
        api_key: CompanyEnrich key; falls back to COMPANYENRICH_API_KEY.
        timeout: Positive finite HTTP timeout in seconds.
    """

    def __init__(self, api_key: str | None = None, timeout: float = 30) -> None:
        self._api_key = _text(
            api_key if api_key is not None else os.getenv("COMPANYENRICH_API_KEY", ""),
            "COMPANYENRICH_API_KEY",
        )
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be positive and finite")
        self._timeout = timeout

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return _result(
            httpx.request(
                method,
                "https://api.companyenrich.com" + path,
                headers={"Authorization": "Bearer " + self._api_key, "Accept": "application/json"},
                params=params,
                json=payload,
                timeout=self._timeout,
                follow_redirects=False,
            )
        )

    async def _arequest(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self._timeout, follow_redirects=False) as client:
            response = await client.request(
                method,
                "https://api.companyenrich.com" + path,
                headers={"Authorization": "Bearer " + self._api_key, "Accept": "application/json"},
                params=params,
                json=payload,
            )
        return _result(response)

    def companyenrich_enrich_company(self, domain: str) -> dict[str, Any]:
        """Get a company's profile by domain. Costs 1 credit per call.

        Args:
            domain: Company domain, such as stripe.com.

        Returns:
            The original company profile as a JSON object.
        """
        return self._request("GET", "/companies/enrich", params={"domain": _text(domain, "domain")})

    async def acompanyenrich_enrich_company(self, domain: str) -> dict[str, Any]:
        """Asynchronously enrich a company domain. Costs 1 credit per call."""
        return await self._arequest(
            "GET", "/companies/enrich", params={"domain": _text(domain, "domain")}
        )

    def companyenrich_search_companies(
        self, semantic_query: str, page: int = 1, page_size: int = 5
    ) -> dict[str, Any]:
        """Find companies by description. Costs 1 credit per result, minimum 1.

        Args:
            semantic_query: Natural-language description of desired companies, up to 500 characters.
            page: Page number starting at 1. page * page_size must not exceed 10000.
            page_size: Results per page, between 1 and 100; defaults to 5.

        Returns:
            One page of results with the original pagination metadata.
        """
        return self._request(
            "POST", "/companies/search", payload=_search_payload(semantic_query, page, page_size)
        )

    async def acompanyenrich_search_companies(
        self, semantic_query: str, page: int = 1, page_size: int = 5
    ) -> dict[str, Any]:
        """Asynchronously search one page. Costs 1 credit per result, minimum 1."""
        return await self._arequest(
            "POST", "/companies/search", payload=_search_payload(semantic_query, page, page_size)
        )

    def companyenrich_similar_companies(
        self, domains: list[str], page: int = 1, page_size: int = 5
    ) -> dict[str, Any]:
        """Find similar companies. Costs 5 credits per result, minimum 5.

        Args:
            domains: One to ten seed company domains.
            page: Page number starting at 1.
            page_size: Results per page, between 1 and 100; defaults to 5.

        Returns:
            One page of results, pagination metadata, and similarity scores.
        """
        return self._request(
            "POST", "/companies/similar", payload=_similar_payload(domains, page, page_size)
        )

    async def acompanyenrich_similar_companies(
        self, domains: list[str], page: int = 1, page_size: int = 5
    ) -> dict[str, Any]:
        """Asynchronously find lookalikes. Costs 5 credits per result, minimum 5."""
        return await self._arequest(
            "POST", "/companies/similar", payload=_similar_payload(domains, page, page_size)
        )
