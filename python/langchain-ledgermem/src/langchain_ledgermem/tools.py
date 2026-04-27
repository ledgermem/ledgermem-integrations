"""Two LangChain `tool`s for memory_search + memory_add.

Use these in LangGraph agents (or any tool-calling LLM chain) when you want
the LLM to decide when to read/write memory rather than always running a
retriever step.
"""

from __future__ import annotations

from typing import Any

from langchain_core.tools import StructuredTool
from ledgermem import LedgerMem
from pydantic import BaseModel, Field


class _SearchArgs(BaseModel):
    query: str = Field(description="Natural-language search query.")
    limit: int = Field(default=8, ge=1, le=20)


class _AddArgs(BaseModel):
    content: str = Field(description="The fact to store.")
    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Optional JSON metadata.",
    )


def build_memory_tools(client: LedgerMem) -> list[StructuredTool]:
    """Return [search_tool, add_tool] bound to the given client."""

    def _search(query: str, limit: int = 8) -> list[dict[str, Any]]:
        res = client.search(query, limit=limit)
        return [
            {
                "id": h.memory_id,
                "content": h.content,
                "score": h.score,
                "source": h.source.model_dump() if h.source else None,
            }
            for h in res.hits
        ]

    def _add(content: str, metadata: dict[str, Any] | None = None) -> dict[str, str]:
        m = client.add(content, metadata=metadata)
        return {"id": m.id, "created": m.created_at.isoformat()}

    return [
        StructuredTool.from_function(
            func=_search,
            name="memory_search",
            description=(
                "Search long-term memory for facts relevant to the query. "
                "Call BEFORE answering anything that depends on remembered context."
            ),
            args_schema=_SearchArgs,
        ),
        StructuredTool.from_function(
            func=_add,
            name="memory_add",
            description=(
                "Store a new atomic fact in long-term memory. "
                "Call whenever the user reveals something durable about themselves."
            ),
            args_schema=_AddArgs,
        ),
    ]
