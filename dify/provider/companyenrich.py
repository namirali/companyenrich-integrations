from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from common.client import CompanyEnrichClient, CompanyEnrichError


class CompanyEnrichProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            CompanyEnrichClient(credentials.get("api_key", "")).verify_credentials()
        except CompanyEnrichError as error:
            raise ToolProviderCredentialValidationError(str(error)) from None
