# llama-index-vector-stores-ledgermem

LlamaIndex retriever backed by [LedgerMem Memory](https://proofly.dev).

```bash
pip install llama-index-vector-stores-ledgermem
```

```python
from llama_index.vector_stores.ledgermem import LedgerMemRetriever
from ledgermem import LedgerMem

retriever = LedgerMemRetriever(
    client=LedgerMem(api_key="...", workspace_id="..."),
    similarity_top_k=8,
)

nodes = retriever.retrieve("what does the user prefer for breakfast?")
for n in nodes:
    print(n.score, n.node.text)
```

## License

MIT
