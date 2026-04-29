"""LangChain BaseRetriever implementation backed by Mnemo."""

from __future__ import annotations

from typing import Any

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from getmnemo import Mnemo


class MnemoRetriever(BaseRetriever):
    """Drop-in retriever for any LangChain chain or LangGraph node.

    Example:
        from langchain_getmnemo import MnemoRetriever

        retriever = MnemoRetriever(
            client=Mnemo(api_key="...", workspace_id="..."),
            k=8,
        )
        docs = retriever.invoke("what does the user prefer for breakfast?")
    """

    client: Mnemo
    k: int = 8
    actor_id: str | None = None

    model_config = {"arbitrary_types_allowed": True}

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,  # noqa: ARG002
    ) -> list[Document]:
        kwargs: dict[str, Any] = {"limit": self.k}
        if self.actor_id:
            kwargs["actor_id"] = self.actor_id
        res = self.client.search(query, **kwargs)
        return [
            Document(
                page_content=hit.content,
                metadata={
                    "memory_id": hit.memory_id,
                    "score": hit.score,
                    "source": hit.source.model_dump() if hit.source else None,
                    **(hit.metadata or {}),
                },
            )
            for hit in res.hits
        ]
