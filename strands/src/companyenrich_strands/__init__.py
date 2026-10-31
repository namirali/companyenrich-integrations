"""CompanyEnrich tools for Strands Agents."""

from collections.abc import Callable
from typing import Any

from pydantic import ValidationError
from strands.tools.decorator import DecoratedFunctionTool, FunctionToolMetadata
from strands.types.tools import AgentTool

from ._client import CompanyEnrichClient, CompanyEnrichOperation


class _StrictToolMetadata(FunctionToolMetadata):
    def validate_input(self, input_data: dict[str, Any]) -> dict[str, Any]:
        # Strands' default validator coerces booleans/numbers and strips top-level
        # Annotated constraints. Validate the model strictly before the paid request.
        values = dict(input_data)
        # JSON supplies enum selectors as strings; resolve only this documented field.
        if "operation" in self.input_model.model_fields and isinstance(
            values.get("operation"), str
        ):
            try:
                values["operation"] = CompanyEnrichOperation(values["operation"])
            except ValueError:
                raise ValueError("Unknown CompanyEnrich operation") from None
        try:
            return self.input_model.model_validate(values, strict=True).model_dump()
        except ValidationError:
            raise ValueError("CompanyEnrich tool inputs must match the declared types") from None


def _strict_tool(function: Callable[..., Any]) -> DecoratedFunctionTool:
    metadata = _StrictToolMetadata(function)
    specification = metadata.extract_metadata()
    return DecoratedFunctionTool(specification["name"], specification, function, metadata)


class CompanyEnrichTools(CompanyEnrichClient):
    """Twelve core tools and an advanced selector, using an internal API key."""

    companyenrich_enrich_company = _strict_tool(CompanyEnrichClient.companyenrich_enrich_company)
    companyenrich_search_companies = _strict_tool(
        CompanyEnrichClient.companyenrich_search_companies
    )
    companyenrich_similar_companies = _strict_tool(
        CompanyEnrichClient.companyenrich_similar_companies
    )
    companyenrich_search_people = _strict_tool(CompanyEnrichClient.companyenrich_search_people)
    companyenrich_lookup_person = _strict_tool(CompanyEnrichClient.companyenrich_lookup_person)
    companyenrich_company_workforce = _strict_tool(
        CompanyEnrichClient.companyenrich_company_workforce
    )
    companyenrich_enrich_company_by_properties = _strict_tool(
        CompanyEnrichClient.companyenrich_enrich_company_by_properties
    )
    companyenrich_enrich_companies_batch = _strict_tool(
        CompanyEnrichClient.companyenrich_enrich_companies_batch
    )
    companyenrich_get_company = _strict_tool(CompanyEnrichClient.companyenrich_get_company)
    companyenrich_get_person = _strict_tool(CompanyEnrichClient.companyenrich_get_person)
    companyenrich_count_companies = _strict_tool(CompanyEnrichClient.companyenrich_count_companies)
    companyenrich_count_similar_companies = _strict_tool(
        CompanyEnrichClient.companyenrich_count_similar_companies
    )
    companyenrich_advanced_operation = _strict_tool(
        CompanyEnrichClient.companyenrich_advanced_operation
    )

    @property
    def tools(self) -> list[AgentTool]:
        """Return the registered tools to pass to strands.Agent(tools=...)."""
        return [
            self.companyenrich_enrich_company,
            self.companyenrich_search_companies,
            self.companyenrich_similar_companies,
            self.companyenrich_search_people,
            self.companyenrich_lookup_person,
            self.companyenrich_company_workforce,
            self.companyenrich_enrich_company_by_properties,
            self.companyenrich_enrich_companies_batch,
            self.companyenrich_get_company,
            self.companyenrich_get_person,
            self.companyenrich_count_companies,
            self.companyenrich_count_similar_companies,
            self.companyenrich_advanced_operation,
        ]


__all__ = ["CompanyEnrichTools"]
