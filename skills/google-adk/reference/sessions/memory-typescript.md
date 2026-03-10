# Memory Service — TypeScript Examples

> **Note:** The source documentation did not include TypeScript code examples for the memory service patterns on this page. The TypeScript SDK (`@google/adk`) does support `MemoryService` — refer to the official ADK TypeScript SDK documentation for equivalent patterns.

The conceptual patterns from the Python examples map to TypeScript as follows:

- `InMemoryMemoryService` — available as `InMemoryMemoryService` from `@google/adk/memory`
- `VertexAiMemoryBankService` — available from `@google/adk/memory`
- `PreloadMemoryTool` / `LoadMemoryTool` — available from `@google/adk/tools`
- `Runner` accepts a `memoryService` option in its config
- `memoryService.addSessionToMemory(session)` and `memoryService.searchMemory(query)` are the key methods
