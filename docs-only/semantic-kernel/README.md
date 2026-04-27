# Semantic Kernel + LedgerMem (samples only)

Microsoft Semantic Kernel doesn't get its own helper package yet — the
KernelFunction wrapper is small enough that copy-pasting the snippet below
into your project is the right call.

If demand grows we'll publish `ledgermem-semantic-kernel` (Python and C#).

## Python

```python
from semantic_kernel.functions import kernel_function
from ledgermem import LedgerMem

class LedgerMemPlugin:
    def __init__(self, client: LedgerMem) -> None:
        self.client = client

    @kernel_function(name="memory_search", description="Search long-term memory.")
    def search(self, query: str, limit: int = 8) -> str:
        res = self.client.search(query, limit=limit)
        return "\n".join(f"({h.score:.2f}) {h.content}" for h in res.hits)

    @kernel_function(name="memory_add", description="Store a new fact.")
    def add(self, content: str) -> str:
        return self.client.add(content).id


# Wire it up:
# kernel = Kernel()
# kernel.add_plugin(LedgerMemPlugin(LedgerMem(api_key=..., workspace_id=...)))
```

## C# (sketch)

```csharp
using LedgerMem;  // hypothetical NuGet package - not yet published
using Microsoft.SemanticKernel;

public sealed class LedgerMemPlugin(LedgerMemClient client)
{
    [KernelFunction("memory_search")]
    [Description("Search long-term memory.")]
    public async Task<string> SearchAsync(string query, int limit = 8)
    {
        var res = await client.SearchAsync(query, limit);
        return string.Join("\n", res.Hits.Select(h => $"({h.Score:F2}) {h.Content}"));
    }
}
```

(C# SDK not shipped yet — call the REST API directly with `HttpClient` until
[github.com/ledgermem/ledgermem-dotnet](https://github.com/ledgermem) lands.)
