"""LlamaIndex retriever backed by Mnemo.

We expose a `BaseRetriever` rather than a full VectorStore because Mnemo
already runs hybrid 7-strategy retrieval server-side — we don't need the
local embedding/index orchestration LlamaIndex assumes for VectorStores.
"""

from __future__ import annotations

from typing import Any

from llama_index.core.callbacks import CallbackManager
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.schema import NodeWithScore, QueryBundle, TextNode
from getmnemo import Mnemo


class MnemoRetriever(BaseRetriever):
    """LlamaIndex retriever that delegates to Mnemo search."""

    def __init__(
        self,
        client: Mnemo,
        *,
        similarity_top_k: int = 8,
        actor_id: str | None = None,
        callback_manager: CallbackManager | None = None,
    ) -> None:
        self._client = client
        self._top_k = similarity_top_k
        self._actor_id = actor_id
        super().__init__(callback_manager=callback_manager)

    def _retrieve(self, query_bundle: QueryBundle) -> list[NodeWithScore]:
        kwargs: dict[str, Any] = {"limit": self._top_k}
        if self._actor_id:
            kwargs["actor_id"] = self._actor_id
        res = self._client.search(query_bundle.query_str, **kwargs)
        return [
            NodeWithScore(
                node=TextNode(
                    id_=hit.memory_id,
                    text=hit.content,
                    metadata={
                        "score": hit.score,
                        "source": hit.source.model_dump() if hit.source else None,
                        **(hit.metadata or {}),
                    },
                ),
                score=hit.score,
            )
            for hit in res.hits
        ]


__all__ = ["MnemoRetriever"]
__version__ = "0.1.0"
