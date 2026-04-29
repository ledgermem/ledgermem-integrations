"""CrewAI BaseTool wrappers for Mnemo Memory."""

from __future__ import annotations

from typing import Any

from crewai_tools import BaseTool
from getmnemo import Mnemo
from pydantic import BaseModel, Field

__version__ = "0.1.0"


class _SearchInput(BaseModel):
    query: str = Field(description="Natural-language search query.")
    limit: int = Field(default=8, ge=1, le=20)


class _AddInput(BaseModel):
    content: str = Field(description="The fact to store.")


class MnemoSearchTool(BaseTool):
    name: str = "memory_search"
    description: str = (
        "Search long-term memory for facts relevant to the query. "
        "Use BEFORE answering anything that depends on remembered context."
    )
    args_schema: type[BaseModel] = _SearchInput

    def __init__(self, client: Mnemo, **data: Any) -> None:
        super().__init__(**data)
        object.__setattr__(self, "_client", client)

    def _run(self, query: str, limit: int = 8) -> list[dict[str, Any]]:
        client: Mnemo = self._client  # type: ignore[attr-defined]
        res = client.search(query, limit=limit)
        return [{"id": h.memory_id, "content": h.content, "score": h.score} for h in res.hits]


class MnemoAddTool(BaseTool):
    name: str = "memory_add"
    description: str = "Store a new atomic fact in long-term memory."
    args_schema: type[BaseModel] = _AddInput

    def __init__(self, client: Mnemo, **data: Any) -> None:
        super().__init__(**data)
        object.__setattr__(self, "_client", client)

    def _run(self, content: str) -> dict[str, str]:
        client: Mnemo = self._client  # type: ignore[attr-defined]
        m = client.add(content)
        return {"id": m.id}


def build_memory_tools(client: Mnemo) -> list[BaseTool]:
    return [MnemoSearchTool(client), MnemoAddTool(client)]


__all__ = ["MnemoSearchTool", "MnemoAddTool", "build_memory_tools"]
