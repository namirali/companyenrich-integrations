from collections.abc import Generator
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from common.actions import invoke


class LookupPersonTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        result = invoke(
            "lookup_person",
            tool_parameters,
            self.runtime.credentials.get("api_key", ""),
        )
        yield self.create_json_message(
            result if isinstance(result, dict) else {"data": result}
        )
