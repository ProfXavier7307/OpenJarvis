"""File read tool — disabled by default for personal safety.

Generic host file reads are too broad for a personal AI assistant. Replace this
stub with a workspace-scoped reader before giving an agent file access.
"""

from __future__ import annotations

from typing import Any

from openjarvis.core.registry import ToolRegistry
from openjarvis.core.types import ToolResult
from openjarvis.tools._stubs import BaseTool, ToolSpec


@ToolRegistry.register("file_read")
class FileReadTool(BaseTool):
    """Disabled generic file read placeholder."""

    tool_id = "file_read"

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="file_read",
            description=(
                "Generic host file reads are disabled in this fork. Create a "
                "workspace-scoped reader before enabling file access."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Requested file path. This fork denies it.",
                    },
                    "max_lines": {
                        "type": "integer",
                        "description": "Ignored while the tool is disabled.",
                    },
                },
                "required": ["path"],
            },
            category="filesystem",
            required_capabilities=["file:read"],
        )

    def execute(self, **params: Any) -> ToolResult:
        path = params.get("path", "")
        return ToolResult(
            tool_name="file_read",
            content=(
                "Denied: generic file reads are disabled in this fork. "
                "Requested path was not read. Use a future workspace-only "
                "reader for files you explicitly choose to expose."
            ),
            success=False,
            metadata={"requested_path": path},
        )


__all__ = ["FileReadTool"]
