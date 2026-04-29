/**
 * Vercel AI SDK helpers for Mnemo Memory.
 *
 * @example
 * ```ts
 * import { generateText } from 'ai'
 * import { openai } from '@ai-sdk/openai'
 * import { Mnemo } from '@getmnemo/memory'
 * import { memoryTools } from '@getmnemo/ai-sdk'
 *
 * const memory = new Mnemo({ apiKey: '...', workspaceId: '...' })
 *
 * await generateText({
 *   model: openai('gpt-4.1-mini'),
 *   tools: memoryTools(memory),
 *   prompt: 'Recall what the user told you last week about rice.',
 * })
 * ```
 */

import type { Mnemo } from '@getmnemo/memory'
import { tool, type Tool } from 'ai'
import { z } from 'zod'

export type MemoryToolset = {
  memory_search: Tool
  memory_add: Tool
}

export function memoryTools(memory: Mnemo): MemoryToolset {
  return {
    memory_search: tool({
      description:
        'Search long-term memory for facts relevant to the query. Use BEFORE answering anything that depends on remembered context.',
      parameters: z.object({
        query: z.string().describe('Natural-language search query.'),
        limit: z.number().int().min(1).max(20).default(8),
      }),
      execute: async ({ query, limit }) => {
        const res = await memory.search({ query, limit })
        return {
          query: res.query,
          latencyMs: res.latencyMs,
          hits: res.hits.map((h) => ({
            id: h.memoryId,
            content: h.content,
            score: h.score,
            source: h.source ?? null,
          })),
        }
      },
    }),
    memory_add: tool({
      description:
        'Store a new atomic fact in long-term memory. Use whenever the user reveals something durable about themselves.',
      parameters: z.object({
        content: z.string(),
        metadata: z.record(z.unknown()).optional(),
      }),
      execute: async ({ content, metadata }) => {
        const m = await memory.add({ content, metadata })
        return { id: m.id, created: m.createdAt }
      },
    }),
  }
}
