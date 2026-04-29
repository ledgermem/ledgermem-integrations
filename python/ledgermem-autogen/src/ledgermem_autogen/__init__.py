"""AutoGen FunctionTool wrappers for Mnemo Memory."""

from __future__ import annotations

from typing import Any

from autogen_core.tools import FunctionTool
from getmnemo import Mnemo

__version__ = "0.1.0"


def build_memory_tools(client: Mnemo) -> list[FunctionTool]:
    """Return [search_tool, add_tool] as AutoGen FunctionTools."""

    async def memory_search(query: str, limit: int = 8) -> list[dict[str, Any]]:
        """Search long-term memory for facts relevant to the query."""
        res = client.search(query, limit=limit)
        return [
            {"id": h.memory_id, "content": h.content, "score": h.score}
            for h in res.hits
        ]

    async def memory_add(content: str) -> dict[str, str]:
        """Store a new atomic fact in long-term memory."""
        m = client.add(content)
        return {"id": m.id}

    return [
        FunctionTool(memory_search, description=memory_search.__doc__ or ""),
        FunctionTool(memory_add, description=memory_add.__doc__ or ""),
    ]


__all__ = ["build_memory_tools"]
