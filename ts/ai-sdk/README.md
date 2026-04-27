# @ledgermem/ai-sdk

[Vercel AI SDK](https://sdk.vercel.ai) helpers for LedgerMem Memory.

```bash
npm install @ledgermem/ai-sdk @ledgermem/memory ai zod
```

```ts
import { generateText } from 'ai'
import { openai } from '@ai-sdk/openai'
import { LedgerMem } from '@ledgermem/memory'
import { memoryTools } from '@ledgermem/ai-sdk'

const memory = new LedgerMem({
  apiKey: process.env.LEDGERMEM_API_KEY!,
  workspaceId: process.env.LEDGERMEM_WORKSPACE_ID!,
})

const { text } = await generateText({
  model: openai('gpt-4.1-mini'),
  tools: memoryTools(memory),
  maxSteps: 5,
  prompt: 'What kind of rice does the user prefer?',
})

console.log(text)
```

## What it gives you

- `memory_search` — returns ranked hits with content, score, and source citations
- `memory_add` — stores a new atomic fact

The model decides when to call them. Standard Vercel AI SDK tool semantics.

## License

MIT
