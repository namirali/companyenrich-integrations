"""CompanyEnrich company and people data toolkit for CAMEL."""

from collections.abc import Awaitable, Callable
from typing import Any

from camel.toolkits import BaseToolkit, FunctionTool

from ._client import CompanyEnrichClient


class _CompanyEnrichFunctionTool(FunctionTool):
    """Use our validated callables directly so CAMEL cannot echo inputs on errors."""

    def __init__(
        self, function: Callable[..., Any], async_function: Callable[..., Awaitable[Any]]
    ) -> None:
        super().__init__(function)
        self._async_function = async_function
        parameters = self.openai_tool_schema["function"]["parameters"]
        operation = parameters["properties"].get("operation", {})
        if "$ref" in operation:
            # Inline the enum so its beta description appears alongside the selector.
            enum = parameters["$defs"][operation["$ref"].rsplit("/", 1)[-1]]
            parameters["properties"]["operation"] = {
                **enum,
                "description": "One of 42 documented operations; Beta email routes require allow_beta=True.",
            }

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)

    async def async_call(self, *args: Any, **kwargs: Any) -> Any:
        return await self._async_function(*args, **kwargs)


class CompanyEnrichToolkit(CompanyEnrichClient, BaseToolkit):
    """Twelve core tools and one advanced selector with internal API credentials."""

    def __init__(self, api_key: str | None = None, timeout: float = 30) -> None:
        BaseToolkit.__init__(self, timeout=timeout)
        CompanyEnrichClient.__init__(self, api_key=api_key, timeout=timeout)

    def get_tools(self) -> list[FunctionTool]:
        """Return the company and people data tools for ChatAgent."""
        return [
            _CompanyEnrichFunctionTool(
                self.companyenrich_enrich_company, self.acompanyenrich_enrich_company
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_search_companies, self.acompanyenrich_search_companies
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_similar_companies, self.acompanyenrich_similar_companies
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_search_people, self.acompanyenrich_search_people
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_lookup_person, self.acompanyenrich_lookup_person
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_company_workforce, self.acompanyenrich_company_workforce
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_enrich_company_by_properties,
                self.acompanyenrich_enrich_company_by_properties,
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_enrich_companies_batch,
                self.acompanyenrich_enrich_companies_batch,
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_get_company, self.acompanyenrich_get_company
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_get_person, self.acompanyenrich_get_person
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_count_companies, self.acompanyenrich_count_companies
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_count_similar_companies,
                self.acompanyenrich_count_similar_companies,
            ),
            _CompanyEnrichFunctionTool(
                self.companyenrich_advanced_operation, self.acompanyenrich_advanced_operation
            ),
        ]


__all__ = ["CompanyEnrichToolkit"]
