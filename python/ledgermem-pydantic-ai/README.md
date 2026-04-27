# ledgermem-pydantic-ai

[Pydantic AI](https://ai.pydantic.dev) Tool wrappers for [LedgerMem Memory](https://proofly.dev).

```bash
pip install ledgermem-pydantic-ai
```

```python
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from ledgermem import AsyncLedgerMem
from ledgermem_pydantic_ai import build_memory_tools

async def main() -> None:
    async with AsyncLedgerMem(api_key="...", workspace_id="...") as memory:
        agent = Agent(
            OpenAIModel("gpt-4.1-mini"),
            tools=build_memory_tools(memory),
        )
        result = await agent.run("What rice does the user prefer?")
        print(result.output)

asyncio.run(main())
```

## License

MIT
