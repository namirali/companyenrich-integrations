"""Bounded, validated CompanyEnrich requests with native sync and async methods."""

import math
import os
from enum import Enum
from typing import Any

import httpx

from ._core import core_arguments
from ._validation import prepare_request


def _text(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")
    return value.strip()


def _page(page: int, page_size: int) -> None:
    if type(page) is not int or type(page_size) is not int:
        raise TypeError("page and page_size must be integers")
    if page < 1 or not 1 <= page_size <= 100:
        raise ValueError("page must be positive and page_size must be between 1 and 100")


def _result(response: httpx.Response) -> Any:
    if not response.is_success:
        # Preserve the familiar HTTP exception/status while omitting input queries, credentials and body.
        safe_request = httpx.Request(response.request.method, "https://api.companyenrich.com")
        safe_response = httpx.Response(response.status_code, request=safe_request)
        raise httpx.HTTPStatusError(
            f"CompanyEnrich returned HTTP {response.status_code}. Check credentials, credits and inputs.",
            request=safe_request,
            response=safe_response,
        ) from None
    try:
        return response.json()
    except ValueError:
        raise ValueError("CompanyEnrich returned invalid JSON") from None


class CompanyEnrichOperation(str, Enum):
    """Fixed public operations; email operations require explicit beta opt-in."""

    get_companies_enrich = "get_companies_enrich"
    post_companies_enrich = "post_companies_enrich"
    post_companies_enrich_batch = "post_companies_enrich_batch"
    get_companies_workforce = "get_companies_workforce"
    get_companies_autocomplete = "get_companies_autocomplete"
    post_companies_enrich_bulk = "post_companies_enrich_bulk"
    get_companies_enrich_bulk_jobid = "get_companies_enrich_bulk_jobid"
    get_companies_enrich_bulk_jobs = "get_companies_enrich_bulk_jobs"
    post_companies_search = "post_companies_search"
    post_companies_search_preview = "post_companies_search_preview"
    post_companies_search_count = "post_companies_search_count"
    post_companies_search_scroll = "post_companies_search_scroll"
    get_companies = "get_companies"
    post_companies_search_async = "post_companies_search_async"
    get_companies_search_async_jobid = "get_companies_search_async_jobid"
    get_companies_search_async_jobs = "get_companies_search_async_jobs"
    post_companies_similar = "post_companies_similar"
    post_companies_similar_preview = "post_companies_similar_preview"
    post_companies_similar_count = "post_companies_similar_count"
    post_companies_similar_scroll = "post_companies_similar_scroll"
    post_people_lookup = "post_people_lookup"
    get_people = "get_people"
    post_people_search = "post_people_search"
    post_people_search_scroll = "post_people_search_scroll"
    get_people_email = "get_people_email"
    post_people_email_bulk = "post_people_email_bulk"
    get_people_email_bulk_jobid = "get_people_email_bulk_jobid"
    get_people_education = "get_people_education"
    post_people_search_async = "post_people_search_async"
    get_people_search_async_jobid = "get_people_search_async_jobid"
    get_people_search_async_jobs = "get_people_search_async_jobs"
    get_jobs = "get_jobs"
    get_jobs_jobid = "get_jobs_jobid"
    get_geo_regions = "get_geo_regions"
    get_geo_countries_countrycode = "get_geo_countries_countrycode"
    post_geo_countries = "post_geo_countries"
    post_geo_states = "post_geo_states"
    post_geo_cities = "post_geo_cities"
    get_industries = "get_industries"
    get_keywords_autocomplete = "get_keywords_autocomplete"
    get_technologies_autocomplete = "get_technologies_autocomplete"
    get_positions_autocomplete = "get_positions_autocomplete"


class CompanyEnrichClient:
    """One bounded request per invocation; credentials never enter tool schemas.

    Args:
        api_key: API key, falling back to COMPANYENRICH_API_KEY.
        timeout: Positive finite HTTP timeout in seconds, default 30.
    """

    def __init__(self, api_key: str | None = None, timeout: float = 30) -> None:
        self._api_key = _text(
            api_key if api_key is not None else os.getenv("COMPANYENRICH_API_KEY", ""),
            "COMPANYENRICH_API_KEY",
        )
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or not math.isfinite(timeout)
            or timeout <= 0
        ):
            raise ValueError("timeout must be positive and finite")
        self._timeout = timeout

    def _request(
        self, method: str, path: str, *, params: dict | None = None, payload: dict | None = None
    ) -> Any:
        try:
            response = httpx.request(
                method,
                "https://api.companyenrich.com" + path,
                headers={"Authorization": "Bearer " + self._api_key, "Accept": "application/json"},
                params=params,
                json=payload,
                timeout=self._timeout,
                follow_redirects=False,
            )
        except httpx.RequestError as exc:
            raise type(exc)(
                "CompanyEnrich request failed. Check connectivity and configuration."
            ) from None
        return _result(response)

    async def _arequest(
        self, method: str, path: str, *, params: dict | None = None, payload: dict | None = None
    ) -> Any:
        try:
            async with httpx.AsyncClient(timeout=self._timeout, follow_redirects=False) as client:
                response = await client.request(
                    method,
                    "https://api.companyenrich.com" + path,
                    headers={
                        "Authorization": "Bearer " + self._api_key,
                        "Accept": "application/json",
                    },
                    params=params,
                    json=payload,
                )
        except httpx.RequestError as exc:
            raise type(exc)(
                "CompanyEnrich request failed. Check connectivity and configuration."
            ) from None
        return _result(response)

    def _prepare_core(self, operation: str, values: dict[str, Any]) -> tuple:
        if operation in {"post_companies_search", "post_companies_similar"}:
            _page(values["page"], values["page_size"])
        if operation == "post_companies_search" and values.get("semantic_query") is not None:
            values["semantic_query"] = _text(values["semantic_query"], "semantic_query")
        if operation == "post_companies_similar" and not isinstance(values["domains"], list):
            raise TypeError("domains must be a list of strings")
        body, query = core_arguments(operation, values)
        return prepare_request(operation, body=body, query=query)

    def _core_result(self, operation: str, result: Any) -> Any:
        if operation in {
            "get_companies_enrich",
            "post_companies_search",
            "post_companies_similar",
        } and not isinstance(result, dict):
            raise ValueError("Expected a JSON object from CompanyEnrich")
        return result

    def _invoke(self, operation: str, values: dict[str, Any]) -> Any:
        method, path, query, body = self._prepare_core(operation, values)
        return self._core_result(operation, self._request(method, path, params=query, payload=body))

    async def _ainvoke(self, operation: str, values: dict[str, Any]) -> Any:
        method, path, query, body = self._prepare_core(operation, values)
        return self._core_result(
            operation, await self._arequest(method, path, params=query, payload=body)
        )

    def companyenrich_enrich_company(
        self,
        domain: str,
        *,
        expand: list[str] | None = None,
        wait_for_enrichment: bool | None = None,
    ) -> Any:
        """Enrich a company domain. Optional workforce expansion can consume extra credits. Data and expansions may consume credits.

        Args:
            domain: Company domain, such as stripe.com.
            expand: Optional ["workforce"] expansion.
            wait_for_enrichment: Whether to wait for pending company enrichment.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("get_companies_enrich", locals())

    async def acompanyenrich_enrich_company(
        self,
        domain: str,
        *,
        expand: list[str] | None = None,
        wait_for_enrichment: bool | None = None,
    ) -> Any:
        """Enrich a company domain. Optional workforce expansion can consume extra credits. Data and expansions may consume credits.

        Args:
            domain: Company domain, such as stripe.com.
            expand: Optional ["workforce"] expansion.
            wait_for_enrichment: Whether to wait for pending company enrichment.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("get_companies_enrich", locals())

    def companyenrich_search_companies(
        self,
        semantic_query: str | None = None,
        page: int = 1,
        page_size: int = 5,
        *,
        query: str | None = None,
        filters: dict[str, Any] | None = None,
        expand: list[str] | None = None,
    ) -> Any:
        """Search companies by semantic description, literal query and structured filters. Data and expansions may consume credits.

        Args:
            semantic_query: Natural-language description, up to 500 characters.
            page: Page starting at 1; page times page_size must not exceed 10000.
            page_size: Results per page from 1 to 100; defaults to 5.
            query: Optional literal search query, up to 250 characters.
            filters: Full documented body filters; dedicated values take precedence.
            expand: Optional ["workforce"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("post_companies_search", locals())

    async def acompanyenrich_search_companies(
        self,
        semantic_query: str | None = None,
        page: int = 1,
        page_size: int = 5,
        *,
        query: str | None = None,
        filters: dict[str, Any] | None = None,
        expand: list[str] | None = None,
    ) -> Any:
        """Search companies by semantic description, literal query and structured filters. Data and expansions may consume credits.

        Args:
            semantic_query: Natural-language description, up to 500 characters.
            page: Page starting at 1; page times page_size must not exceed 10000.
            page_size: Results per page from 1 to 100; defaults to 5.
            query: Optional literal search query, up to 250 characters.
            filters: Full documented body filters; dedicated values take precedence.
            expand: Optional ["workforce"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("post_companies_search", locals())

    def companyenrich_similar_companies(
        self,
        domains: list[str],
        page: int = 1,
        page_size: int = 5,
        *,
        filters: dict[str, Any] | None = None,
        expand: list[str] | None = None,
        wait_for_enrichment: bool | None = None,
    ) -> Any:
        """Find lookalike companies using one to ten seed domains and optional filters. Data and expansions may consume credits.

        Args:
            domains: One to ten seed domains.
            page: Page starting at 1; page times page_size must not exceed 10000.
            page_size: Results per page from 1 to 100; defaults to 5.
            filters: Full documented body filters; dedicated values take precedence.
            expand: Optional ["workforce"] expansion.
            wait_for_enrichment: Whether to wait for pending company enrichment.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("post_companies_similar", locals())

    async def acompanyenrich_similar_companies(
        self,
        domains: list[str],
        page: int = 1,
        page_size: int = 5,
        *,
        filters: dict[str, Any] | None = None,
        expand: list[str] | None = None,
        wait_for_enrichment: bool | None = None,
    ) -> Any:
        """Find lookalike companies using one to ten seed domains and optional filters. Data and expansions may consume credits.

        Args:
            domains: One to ten seed domains.
            page: Page starting at 1; page times page_size must not exceed 10000.
            page_size: Results per page from 1 to 100; defaults to 5.
            filters: Full documented body filters; dedicated values take precedence.
            expand: Optional ["workforce"] expansion.
            wait_for_enrichment: Whether to wait for pending company enrichment.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("post_companies_similar", locals())

    def companyenrich_search_people(
        self,
        filters: dict[str, Any],
        page: int = 1,
        page_size: int = 5,
        *,
        expand: list[str] | None = None,
    ) -> Any:
        """Search people with role, company, geography, seniority and education filters. Data and expansions may consume credits.

        Args:
            filters: Documented people search filters, including query and companyFilter.
            page: Page starting at 1.
            page_size: Results per page from 1 to 100; defaults to 5.
            expand: Optional ["education"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("post_people_search", locals())

    async def acompanyenrich_search_people(
        self,
        filters: dict[str, Any],
        page: int = 1,
        page_size: int = 5,
        *,
        expand: list[str] | None = None,
    ) -> Any:
        """Search people with role, company, geography, seniority and education filters. Data and expansions may consume credits.

        Args:
            filters: Documented people search filters, including query and companyFilter.
            page: Page starting at 1.
            page_size: Results per page from 1 to 100; defaults to 5.
            expand: Optional ["education"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("post_people_search", locals())

    def companyenrich_lookup_person(self, email: str, *, expand: list[str] | None = None) -> Any:
        """Look up a person and company from an email address. Data and expansions may consume credits.

        Args:
            email: Nonempty email address.
            expand: Optional ["education"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("post_people_lookup", locals())

    async def acompanyenrich_lookup_person(
        self, email: str, *, expand: list[str] | None = None
    ) -> Any:
        """Look up a person and company from an email address. Data and expansions may consume credits.

        Args:
            email: Nonempty email address.
            expand: Optional ["education"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("post_people_lookup", locals())

    def companyenrich_company_workforce(
        self, company_id: str | None = None, domain: str | None = None
    ) -> Any:
        """Retrieve workforce data using exactly one company UUID or domain. Data and expansions may consume credits.

        Args:
            company_id: Company UUID; omit when using domain.
            domain: Company domain; omit when using company_id.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("get_companies_workforce", locals())

    async def acompanyenrich_company_workforce(
        self, company_id: str | None = None, domain: str | None = None
    ) -> Any:
        """Retrieve workforce data using exactly one company UUID or domain. Data and expansions may consume credits.

        Args:
            company_id: Company UUID; omit when using domain.
            domain: Company domain; omit when using company_id.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("get_companies_workforce", locals())

    def companyenrich_enrich_company_by_properties(
        self, properties: dict[str, Any], *, expand: list[str] | None = None
    ) -> Any:
        """Match a company by name or documented social properties. Data and expansions may consume credits.

        Args:
            properties: At least one of name, linkedinUrl, linkedinId, twitterUrl, facebookUrl, instagramUrl, or youTubeUrl.
            expand: Optional ["workforce"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("post_companies_enrich", locals())

    async def acompanyenrich_enrich_company_by_properties(
        self, properties: dict[str, Any], *, expand: list[str] | None = None
    ) -> Any:
        """Match a company by name or documented social properties. Data and expansions may consume credits.

        Args:
            properties: At least one of name, linkedinUrl, linkedinId, twitterUrl, facebookUrl, instagramUrl, or youTubeUrl.
            expand: Optional ["workforce"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("post_companies_enrich", locals())

    def companyenrich_enrich_companies_batch(
        self, domains: list[str], *, expand: list[str] | None = None
    ) -> Any:
        """Enrich one to fifty company domains in one request. Data and expansions may consume credits.

        Args:
            domains: One to fifty nonempty company domains.
            expand: Optional ["workforce"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("post_companies_enrich_batch", locals())

    async def acompanyenrich_enrich_companies_batch(
        self, domains: list[str], *, expand: list[str] | None = None
    ) -> Any:
        """Enrich one to fifty company domains in one request. Data and expansions may consume credits.

        Args:
            domains: One to fifty nonempty company domains.
            expand: Optional ["workforce"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("post_companies_enrich_batch", locals())

    def companyenrich_get_company(self, company_id: str, *, expand: list[str] | None = None) -> Any:
        """Retrieve a company by UUID. Data and expansions may consume credits.

        Args:
            company_id: Company UUID.
            expand: Optional ["workforce"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("get_companies", locals())

    async def acompanyenrich_get_company(
        self, company_id: str, *, expand: list[str] | None = None
    ) -> Any:
        """Retrieve a company by UUID. Data and expansions may consume credits.

        Args:
            company_id: Company UUID.
            expand: Optional ["workforce"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("get_companies", locals())

    def companyenrich_get_person(
        self, person_id: str | int, *, expand: list[str] | None = None
    ) -> Any:
        """Retrieve a person by positive int64 ID. Data and expansions may consume credits.

        Args:
            person_id: Positive int64 ID; a decimal string preserves precision.
            expand: Optional ["education"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("get_people", locals())

    async def acompanyenrich_get_person(
        self, person_id: str | int, *, expand: list[str] | None = None
    ) -> Any:
        """Retrieve a person by positive int64 ID. Data and expansions may consume credits.

        Args:
            person_id: Positive int64 ID; a decimal string preserves precision.
            expand: Optional ["education"] expansion.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("get_people", locals())

    def companyenrich_count_companies(
        self,
        semantic_query: str | None = None,
        *,
        query: str | None = None,
        filters: dict[str, Any] | None = None,
    ) -> Any:
        """Count companies matching a search, preserving zero results. Data and expansions may consume credits.

        Args:
            semantic_query: Optional semantic description, up to 500 characters.
            query: Optional literal query, up to 250 characters.
            filters: Full documented search filters; dedicated values take precedence.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("post_companies_search_count", locals())

    async def acompanyenrich_count_companies(
        self,
        semantic_query: str | None = None,
        *,
        query: str | None = None,
        filters: dict[str, Any] | None = None,
    ) -> Any:
        """Count companies matching a search, preserving zero results. Data and expansions may consume credits.

        Args:
            semantic_query: Optional semantic description, up to 500 characters.
            query: Optional literal query, up to 250 characters.
            filters: Full documented search filters; dedicated values take precedence.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("post_companies_search_count", locals())

    def companyenrich_count_similar_companies(
        self,
        domains: list[str],
        *,
        filters: dict[str, Any] | None = None,
        wait_for_enrichment: bool | None = None,
    ) -> Any:
        """Count companies similar to one to ten seed domains. Data and expansions may consume credits.

        Args:
            domains: One to ten seed domains.
            filters: Full documented lookalike filters.
            wait_for_enrichment: Whether to wait for pending company enrichment.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return self._invoke("post_companies_similar_count", locals())

    async def acompanyenrich_count_similar_companies(
        self,
        domains: list[str],
        *,
        filters: dict[str, Any] | None = None,
        wait_for_enrichment: bool | None = None,
    ) -> Any:
        """Count companies similar to one to ten seed domains. Data and expansions may consume credits.

        Args:
            domains: One to ten seed domains.
            filters: Full documented lookalike filters.
            wait_for_enrichment: Whether to wait for pending company enrichment.

        Returns:
            Full API response, including metadata and future nested fields.
        """
        return await self._ainvoke("post_companies_similar_count", locals())

    def companyenrich_advanced_operation(
        self,
        operation: CompanyEnrichOperation,
        *,
        body: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
        path_parameters: dict[str, Any] | None = None,
        allow_beta: bool = False,
    ) -> Any:
        """Make one allowlisted request; beta email operations require explicit opt-in.

        Args:
            operation: One of 42 documented fixed method/path operations. Email routes are Beta.
            body: Documented JSON body. Export jobs require count from 1 to 50000.
            query: Documented URL query parameters only.
            path_parameters: Documented path fields such as jobId or countryCode.
            allow_beta: Explicit permission for Beta email operations; defaults to False.

        Returns:
            Complete JSON response, including arrays and numeric counts. Job IDs, cursors
            and result URLs are returned without automatic polling or downloading.
        """
        method, path, params, payload = prepare_request(
            operation,
            body=body,
            query=query,
            path_parameters=path_parameters,
            allow_beta=allow_beta,
        )
        return self._request(method, path, params=params, payload=payload)

    async def acompanyenrich_advanced_operation(
        self,
        operation: CompanyEnrichOperation,
        *,
        body: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
        path_parameters: dict[str, Any] | None = None,
        allow_beta: bool = False,
    ) -> Any:
        """Make one allowlisted request; beta email operations require explicit opt-in.

        Args:
            operation: One of 42 documented fixed method/path operations. Email routes are Beta.
            body: Documented JSON body. Export jobs require count from 1 to 50000.
            query: Documented URL query parameters only.
            path_parameters: Documented path fields such as jobId or countryCode.
            allow_beta: Explicit permission for Beta email operations; defaults to False.

        Returns:
            Complete JSON response, including arrays and numeric counts. Job IDs, cursors
            and result URLs are returned without automatic polling or downloading.
        """
        method, path, params, payload = prepare_request(
            operation,
            body=body,
            query=query,
            path_parameters=path_parameters,
            allow_beta=allow_beta,
        )
        return await self._arequest(method, path, params=params, payload=payload)
