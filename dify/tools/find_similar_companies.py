from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from common.client import CompanyEnrichClient


class FindSimilarCompaniesTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        client = CompanyEnrichClient(self.runtime.credentials.get("api_key", ""))
        result = client.find_similar_companies(
            tool_parameters.get("domains", ""),
            tool_parameters.get("page", 1),
            tool_parameters.get("page_size", 10),
        )
        yield self.create_json_message(result)
