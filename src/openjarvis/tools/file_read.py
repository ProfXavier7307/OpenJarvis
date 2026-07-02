"""File read tool — read only from the local Personal-Memory directory.

This fork intentionally limits agent-readable files to a single folder named
``Personal-Memory`` at the OpenJarvis repository/install root. This gives the
assistant useful memory access without exposing the rest of the host filesystem.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from openjarvis.core.registry import ToolRegistry
from openjarvis.core.types import ToolResult
from openjarvis.tools._stubs import BaseTool, ToolSpec

# Maximum file size to read (1 MB)
_MAX_SIZE_BYTES = 1_048_576
_MEMORY_DIR_NAME = "Personal-Memory"


def _repo_root() -> Path:
    """Return the OpenJarvis source/repository root for an editable install."""
    # src/openjarvis/tools/file_read.py -> repo root is parents[3]
    return Path(__file__).resolve().parents[3]


def _memory_root() -> Path:
    return (_repo_root() / _MEMORY_DIR_NAME).resolve()


def _resolve_memory_path(raw_path: str) -> Path:
    """Resolve a requested path inside Personal-Memory.

    Relative paths are treated as paths inside Personal-Memory, so requesting
    ``notes.md`` resolves to ``Personal-Memory/notes.md``. Requests that already
    begin with ``Personal-Memory`` also work. Absolute paths are allowed only if
    they resolve inside Personal-Memory.
    """
    requested = Path(raw_path)
    root = _memory_root()

    if requested.is_absolute():
        return requested.resolve()

    parts = requested.parts
    if parts and parts[0] == _MEMORY_DIR_NAME:
        return (_repo_root() / requested).resolve()

    return (root / requested).resolve()


def _is_inside_memory(path: Path) -> bool:
    root = _memory_root()
    resolved = path.resolve()
    return resolved == root or resolved.is_relative_to(root)


@ToolRegistry.register("file_read")
class FileReadTool(BaseTool):
    """Read files only from the Personal-Memory folder."""

    tool_id = "file_read"

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="file_read",
            description=(
                "Read a file from the local Personal-Memory directory only. "
                "Relative paths are resolved inside Personal-Memory."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": (
                            "File path inside Personal-Memory, such as "
                            "notes.md or projects/doa.md."
                        ),
                    },
                    "max_lines": {
                        "type": "integer",
                        "description": "Max lines to return (default: all).",
                    },
                },
                "required": ["path"],
            },
            category="filesystem",
            required_capabilities=["file:read"],
        )

    def execute(self, **params: Any) -> ToolResult:
        raw_path = params.get("path", "")
        if not raw_path:
            return ToolResult(
                tool_name="file_read",
                content="No path provided.",
                success=False,
            )

        path = _resolve_memory_path(raw_path)
        root = _memory_root()

        if not _is_inside_memory(path):
            return ToolResult(
                tool_name="file_read",
                content=(
                    "Access denied: file_read can only read files inside "
                    f"{root}."
                ),
                success=False,
                metadata={"requested_path": raw_path, "memory_root": str(root)},
            )

        # Block sensitive files even inside Personal-Memory.
        from openjarvis.security.file_policy import is_sensitive_file

        if is_sensitive_file(path):
            return ToolResult(
                tool_name="file_read",
                content=f"Access denied: {raw_path} is a sensitive file type.",
                success=False,
            )

        if not path.exists():
            return ToolResult(
                tool_name="file_read",
                content=f"File not found in Personal-Memory: {raw_path}",
                success=False,
                metadata={"memory_root": str(root)},
            )
        if not path.is_file():
            return ToolResult(
                tool_name="file_read",
                content=f"Not a file inside Personal-Memory: {raw_path}",
                success=False,
            )

        try:
            size = path.stat().st_size
        except OSError as exc:
            return ToolResult(
                tool_name="file_read",
                content=f"Cannot stat file: {exc}",
                success=False,
            )
        if size > _MAX_SIZE_BYTES:
            return ToolResult(
                tool_name="file_read",
                content=f"File too large: {size} bytes (max {_MAX_SIZE_BYTES}).",
                success=False,
            )

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return ToolResult(
                tool_name="file_read",
                content=f"Read error: {exc}",
                success=False,
            )

        max_lines = params.get("max_lines")
        if max_lines is not None:
            try:
                max_lines = int(max_lines)
            except (TypeError, ValueError):
                max_lines = None
        if max_lines is not None and max_lines > 0:
            lines = text.splitlines(keepends=True)
            text = "".join(lines[:max_lines])

        return ToolResult(
            tool_name="file_read",
            content=text,
            success=True,
            metadata={
                "path": str(path),
                "memory_root": str(root),
                "size_bytes": size,
            },
        )


__all__ = ["FileReadTool"]
