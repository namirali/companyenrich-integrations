from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from common.client import CompanyEnrichClient


class EnrichCompanyTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        client = CompanyEnrichClient(self.runtime.credentials.get("api_key", ""))
        result = client.enrich_company(tool_parameters.get("domain", ""))
        yield self.create_json_message(result)
