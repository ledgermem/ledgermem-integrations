# ledgermem-crewai

[CrewAI](https://github.com/crewAIInc/crewAI) BaseTool wrappers for [LedgerMem Memory](https://proofly.dev).

```bash
pip install ledgermem-crewai
```

```python
from crewai import Agent, Task, Crew
from ledgermem import LedgerMem
from ledgermem_crewai import build_memory_tools

memory = LedgerMem(api_key="...", workspace_id="...")
research_agent = Agent(
    role="researcher",
    goal="Recall and write up everything we know about the user.",
    tools=build_memory_tools(memory),
)
```

## License

MIT
