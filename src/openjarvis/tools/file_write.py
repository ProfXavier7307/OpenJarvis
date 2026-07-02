"""File write tool — disabled by default for personal safety.

Generic host file writes are too broad for a personal AI assistant. Replace this
stub with a workspace-scoped writer before giving an agent file access.
"""

from __future__ import annotations

from typing import Any

from openjarvis.core.registry import ToolRegistry
from openjarvis.core.types import ToolResult
from openjarvis.tools._stubs import BaseTool, ToolSpec


@ToolRegistry.register("file_write")
class FileWriteTool(BaseTool):
    """Disabled generic file write placeholder."""

    tool_id = "file_write"

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="file_write",
            description=(
                "Generic host file writes are disabled in this fork. Create a "
                "workspace-scoped writer before enabling file modifications."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Requested file path. This fork denies it.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Requested content. This fork denies it.",
                    },
                    "mode": {
                        "type": "string",
                        "description": "Ignored while the tool is disabled.",
                    },
                    "create_dirs": {
                        "type": "boolean",
                        "description": "Ignored while the tool is disabled.",
                    },
                },
                "required": ["path", "content"],
            },
            category="filesystem",
            required_capabilities=["file:write"],
        )

    def execute(self, **params: Any) -> ToolResult:
        path = params.get("path", "")
        return ToolResult(
            tool_name="file_write",
            content=(
                "Denied: generic file writes are disabled in this fork. "
                "Requested path was not modified. Use a future workspace-only "
                "writer for files you explicitly choose to expose."
            ),
            success=False,
            metadata={"requested_path": path},
        )


__all__ = ["FileWriteTool"]
