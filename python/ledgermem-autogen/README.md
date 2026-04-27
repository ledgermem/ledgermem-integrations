# ledgermem-autogen

[AutoGen v0.4+](https://microsoft.github.io/autogen/) FunctionTool wrappers for [LedgerMem Memory](https://proofly.dev).

```bash
pip install ledgermem-autogen
```

```python
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from ledgermem import LedgerMem
from ledgermem_autogen import build_memory_tools

memory = LedgerMem(api_key="...", workspace_id="...")
agent = AssistantAgent(
    name="memory_aware",
    model_client=OpenAIChatCompletionClient(model="gpt-4.1-mini"),
    tools=build_memory_tools(memory),
)
```

## License

MIT
