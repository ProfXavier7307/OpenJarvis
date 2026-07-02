"""Shell execution tool — disabled by default for personal safety.

This fork intentionally does not allow agents to run arbitrary host shell
commands. Re-enable only after replacing this stub with a narrow allowlist of
specific commands you personally trust.
"""

from __future__ import annotations

from typing import Any

from openjarvis.core.registry import ToolRegistry
from openjarvis.core.types import ToolResult
from openjarvis.tools._stubs import BaseTool, ToolSpec


@ToolRegistry.register("shell_exec")
class ShellExecTool(BaseTool):
    """Disabled shell execution placeholder.

    Host shell access is one of the highest-risk capabilities for a personal AI.
    This tool remains registered so configs that reference shell_exec fail closed
    with a clear message instead of silently becoming an unknown tool.
    """

    tool_id = "shell_exec"

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="shell_exec",
            description=(
                "Host shell execution is disabled in this fork. Replace this "
                "tool with a narrow command allowlist before enabling it."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Requested shell command. This fork denies it.",
                    },
                },
                "required": ["command"],
            },
            category="system",
            requires_confirmation=True,
            timeout_seconds=1.0,
            required_capabilities=["code:execute"],
        )

    def execute(self, **params: Any) -> ToolResult:
        command = params.get("command", "")
        return ToolResult(
            tool_name="shell_exec",
            content=(
                "Denied: host shell execution is disabled in this fork. "
                "Requested command was not run. "
                "For safer automation, create a dedicated tool that exposes "
                "only one approved action instead of arbitrary shell access."
            ),
            success=False,
            metadata={"requested_command": command},
        )


__all__ = ["ShellExecTool"]
