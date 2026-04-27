"""Pydantic AI Tool wrappers for LedgerMem Memory.

Pydantic AI is type-driven; we expose simple async functions that the agent
can register as tools via `Agent(tools=[...])`.
"""

from __future__ import annotations

from typing import Any

from ledgermem import AsyncLedgerMem
from pydantic_ai import RunContext, Tool

__version__ = "0.1.0"


def build_memory_tools(client: AsyncLedgerMem) -> list[Tool[Any]]:
    """Return [search, add] as Pydantic AI Tools.

    Caller owns `client` lifecycle — make sure to `await client.aclose()` when done.
    """

    async def memory_search(
        _ctx: RunContext[Any], query: str, limit: int = 8
    ) -> list[dict[str, Any]]:
        """Search long-term memory for facts relevant to the query."""
        res = await client.search(query, limit=limit)
        return [
            {"id": h.memory_id, "content": h.content, "score": h.score}
            for h in res.hits
        ]

    async def memory_add(_ctx: RunContext[Any], content: str) -> dict[str, str]:
        """Store a new atomic fact in long-term memory."""
        m = await client.add(content)
        return {"id": m.id}

    return [Tool(memory_search), Tool(memory_add)]


__all__ = ["build_memory_tools"]
