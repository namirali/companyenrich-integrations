import math
from typing import Any

import requests


class CompanyEnrichError(ValueError):
    """A sanitized error suitable for displaying in Dify."""


class CompanyEnrichClient:
    def __init__(self, api_key: str):
        if not isinstance(api_key, str) or not api_key.strip():
            raise CompanyEnrichError("A CompanyEnrich API key is required.")
        self._api_key = api_key.strip()

    def verify_credentials(self) -> None:
        self._request("GET", "/me")

    def enrich_company(self, domain: str) -> dict[str, Any]:
        return self._request(
            "GET", "/companies/enrich", params={"domain": self._text(domain, "Domain")}
        )

    def search_companies(
        self, query: str, page: Any = 1, page_size: Any = 10
    ) -> dict[str, Any]:
        query = self._text(query, "Query")
        if len(query) > 500:
            raise CompanyEnrichError("Query must be at most 500 characters.")
        page, page_size = self._pagination(page, page_size)
        return self._request(
            "POST",
            "/companies/search",
            json={"semanticQuery": query, "page": page, "pageSize": page_size},
        )

    def find_similar_companies(
        self, domains: str, page: Any = 1, page_size: Any = 10
    ) -> dict[str, Any]:
        seeds = [part.strip() for part in self._text(domains, "Domains").split(",")]
        if not 1 <= len(seeds) <= 10 or any(not seed for seed in seeds):
            raise CompanyEnrichError(
                "Supply one to ten nonempty company domains separated by commas."
            )
        page, page_size = self._pagination(page, page_size)
        return self._request(
            "POST",
            "/companies/similar",
            json={"domains": seeds, "page": page, "pageSize": page_size},
        )

    @staticmethod
    def _text(value: str, label: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise CompanyEnrichError(f"{label} is required.")
        return value.strip()

    @staticmethod
    def _pagination(page: Any, page_size: Any) -> tuple[int, int]:
        # Dify number parameters can arrive as floats; reject fractions and booleans.
        if any(
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value != int(value)
            for value in (page, page_size)
        ):
            raise CompanyEnrichError("Page and page size must be whole numbers.")
        page, page_size = int(page), int(page_size)
        if page < 1 or not 1 <= page_size <= 100 or page * page_size > 10000:
            raise CompanyEnrichError(
                "Use a positive page and a page size from 1 to 100; page × page size must not exceed 10,000."
            )
        return page, page_size

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        try:
            response = requests.request(
                method,
                f"https://api.companyenrich.com{path}",
                headers={"Authorization": f"Bearer {self._api_key}"},
                timeout=(5, 30),
                allow_redirects=False,
                **kwargs,
            )
        except requests.RequestException:
            raise CompanyEnrichError(
                "CompanyEnrich could not be reached. Check the connection and try again."
            ) from None
        if not 200 <= response.status_code < 300:
            raise CompanyEnrichError(
                f"CompanyEnrich returned HTTP {response.status_code}. Check the API key, available credits, and request parameters."
            )
        try:
            data = response.json()
        except ValueError:
            raise CompanyEnrichError("CompanyEnrich returned invalid JSON.") from None
        if not isinstance(data, dict):
            raise CompanyEnrichError(
                "CompanyEnrich returned an unexpected response format."
            )
        return data
