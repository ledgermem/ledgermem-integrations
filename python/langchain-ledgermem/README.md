# langchain-ledgermem

LangChain + LangGraph integration for [LedgerMem Memory](https://proofly.dev).

```bash
pip install langchain-ledgermem
```

## Use as a retriever

```python
from langchain_ledgermem import LedgerMemRetriever
from ledgermem import LedgerMem

retriever = LedgerMemRetriever(
    client=LedgerMem(api_key="...", workspace_id="..."),
    k=8,
)

docs = retriever.invoke("what does the user prefer for breakfast?")
```

## Use as tools (LangGraph agents)

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from ledgermem import LedgerMem
from langchain_ledgermem import build_memory_tools

memory = LedgerMem(api_key="...", workspace_id="...")
tools = build_memory_tools(memory)

agent = create_react_agent(ChatOpenAI(model="gpt-4.1-mini"), tools)
agent.invoke({"messages": [("user", "What rice does the user prefer?")]})
```

## License

MIT
