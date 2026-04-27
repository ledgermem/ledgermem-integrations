# ledgermem-integrations

Monorepo of helper packages that wire [LedgerMem Memory](https://proofly.dev) into popular agent frameworks.

## Layout

```
ts/                              ← npm workspaces (TypeScript)
  ai-sdk/                        @ledgermem/ai-sdk          (Vercel AI SDK)
python/                          ← independently versioned (each its own pyproject)
  langchain-ledgermem/           langchain-ledgermem        (LangChain + LangGraph)
  llama-index-vector-stores-ledgermem/  llama-index-vector-stores-ledgermem
  ledgermem-autogen/             ledgermem-autogen          (AutoGen v0.4+)
  ledgermem-crewai/              ledgermem-crewai
  ledgermem-pydantic-ai/         ledgermem-pydantic-ai      (Pydantic AI)
docs-only/                       ← Semantic Kernel + others (samples, no helper pkg yet)
```

## Status

| Package | Status | npm / PyPI |
|---|---|---|
| `@ledgermem/ai-sdk` | scaffold | not yet |
| `langchain-ledgermem` | scaffold | not yet |
| `llama-index-vector-stores-ledgermem` | scaffold | not yet |
| `ledgermem-autogen` | scaffold | not yet |
| `ledgermem-crewai` | scaffold | not yet |
| `ledgermem-pydantic-ai` | scaffold | not yet |
| Semantic Kernel | docs-only | n/a |

Each subpackage has its own README, build, and tests. Releases are tagged independently with the form `<pkg>-v<version>`.

## Develop

The TypeScript packages use npm workspaces. The Python packages are independent — `cd` into each and `pip install -e ".[dev]"`.

```bash
# Top of monorepo: install all TS workspaces
npm install
npm run build

# A specific Python package
cd python/langchain-ledgermem
pip install -e ".[dev]"
pytest
```

## License

MIT
