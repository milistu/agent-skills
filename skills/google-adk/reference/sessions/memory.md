# Memory: Long-Term Knowledge with `MemoryService`

We've seen how `Session` tracks the history (`events`) and temporary data (`state`) for a *single, ongoing conversation*. But what if an agent needs to recall information from *past* conversations? This is where the concept of **Long-Term Knowledge** and the **`MemoryService`** come into play.

Think of it this way:

* **`Session` / `State`:** Like your short-term memory during one specific chat.
* **Long-Term Knowledge (`MemoryService`)**: Like a searchable archive or knowledge library the agent can consult, potentially containing information from many past chats or other sources.

## The `MemoryService` Role

The `BaseMemoryService` defines the interface for managing this searchable, long-term knowledge store. Its primary responsibilities are:

1. **Ingesting Information (`add_session_to_memory`):** Taking the contents of a (usually completed) `Session` and adding relevant information to the long-term knowledge store.
2. **Searching Information (`search_memory`):** Allowing an agent (typically via a `Tool`) to query the knowledge store and retrieve relevant snippets or context based on a search query.

## Choosing the Right Memory Service

The ADK offers two distinct `MemoryService` implementations, each tailored to different use cases. Use the table below to decide which is the best fit for your agent.

| **Feature** | **InMemoryMemoryService** | **VertexAiMemoryBankService** |
| --- | --- | --- |
| **Persistence** | None (data is lost on restart) | Yes (Managed by Vertex AI) |
| **Primary Use Case** | Prototyping, local development, and simple testing. | Building meaningful, evolving memories from user conversations. |
| **Memory Extraction** | Stores full conversation | Extracts meaningful information from conversations and consolidates it with existing memories (powered by LLM) |
| **Search Capability** | Basic keyword matching. | Advanced semantic search. |
| **Setup Complexity** | None. It's the default. | Low. Requires an Agent Engine instance in Vertex AI. |
| **Dependencies** | None. | Google Cloud Project, Vertex AI API |
| **When to use it** | When you want to search across multiple sessions’ chat histories for prototyping. | When you want your agent to remember and learn from past interactions. |

## In-Memory Memory

The `InMemoryMemoryService` stores session information in the application's memory and performs basic keyword matching for searches. It requires no setup and is best for prototyping and simple testing scenarios where persistence isn't required.

**Example: Adding and Searching Memory**

This example demonstrates the basic flow using the `InMemoryMemoryService` for simplicity. It shows two runners sharing the same `session_service` and `memory_service`: the first runner captures information and calls `add_session_to_memory`, the second runner uses the `load_memory` tool (or equivalent) in a new session to recall that information.

> *Code examples: see [memory-python.md](memory-python.md), [memory-typescript.md](memory-typescript.md), [memory-go.md](memory-go.md), [memory-java.md](memory-java.md)*

### Searching Memory Within a Tool

You can also search memory from within a custom tool by using the `tool.Context` (Go) or `ToolContext` (Java). This gives a tool direct access to `SearchMemory` / `searchMemory` without going through the built-in `load_memory` tool.

> *Code examples: see [memory-go.md](memory-go.md), [memory-java.md](memory-java.md)*

## Vertex AI Memory Bank

The `VertexAiMemoryBankService` connects your agent to Vertex AI Memory Bank, a fully managed Google Cloud service that provides sophisticated, persistent memory capabilities for conversational agents.

### How It Works

The service handles two key operations:

* **Generating Memories:** At the end of a conversation, you can send the session's events to the Memory Bank, which intelligently processes and stores the information as "memories."
* **Retrieving Memories:** Your agent code can issue a search query against the Memory Bank to retrieve relevant memories from past conversations.

### Prerequisites

Before you can use this feature, you must have:

1. **A Google Cloud Project:** With the Vertex AI API enabled.
2. **An Agent Engine:** You need to create an Agent Engine in Vertex AI. You do not need to deploy your agent to Agent Engine Runtime to use Memory Bank. This will provide you with the **Agent Engine ID** required for configuration.
3. **Authentication:** Ensure your local environment is authenticated to access Google Cloud services. The simplest way is to run `gcloud auth application-default login`.
4. **Environment Variables:** The service requires your Google Cloud Project ID and Location:
   - `GOOGLE_CLOUD_PROJECT="your-gcp-project-id"`
   - `GOOGLE_CLOUD_LOCATION="your-gcp-location"`

### Configuration

To connect your agent to the Memory Bank, use the `--memory_service_uri` flag when starting the ADK server (`adk web` or `adk api_server`). The URI must be in the format `agentengine://<agent_engine_id>`:

```
adk web path/to/your/agents_dir --memory_service_uri="agentengine://1234567890"
```

Or, you can configure your agent to use the Memory Bank by manually instantiating the `VertexAiMemoryBankService` and passing it to the `Runner`.

> *Code examples: see [memory-python.md](memory-python.md), [memory-typescript.md](memory-typescript.md), [memory-go.md](memory-go.md), [memory-java.md](memory-java.md)*

## Using Memory in Your Agent

When a memory service is configured, your agent can use a tool or callback to retrieve memories. ADK includes two pre-built tools for retrieving memories:

* `PreloadMemoryTool`: Always retrieve memory at the beginning of each turn (similar to a callback).
* `LoadMemoryTool`: Retrieve memory when your agent decides it would be helpful.

Include either tool in the agent's `tools=[]` list. To extract memories from your session, call `add_session_to_memory`. You can automate this via an `after_agent_callback` so every completed session is saved to memory automatically.

> *Code examples: see [memory-python.md](memory-python.md), [memory-typescript.md](memory-typescript.md), [memory-go.md](memory-go.md), [memory-java.md](memory-java.md)*

## Advanced Concepts

### How Memory Works in Practice

The memory workflow internally involves these steps:

1. **Session Interaction:** A user interacts with an agent via a `Session`, managed by a `SessionService`. Events are added, and state might be updated.
2. **Ingestion into Memory:** At some point (often when a session is considered complete or has yielded significant information), your application calls `memory_service.add_session_to_memory(session)`. This extracts relevant information from the session's events and adds it to the long-term knowledge store (in-memory dictionary or Agent Engine Memory Bank).
3. **Later Query:** In a *different* (or the same) session, the user might ask a question requiring past context (e.g., "What did we discuss about project X last week?").
4. **Agent Uses Memory Tool:** An agent equipped with a memory-retrieval tool (like the built-in `load_memory` tool) recognizes the need for past context. It calls the tool, providing a search query (e.g., "discussion project X last week").
5. **Search Execution:** The tool internally calls `memory_service.search_memory(app_name, user_id, query)`.
6. **Results Returned:** The `MemoryService` searches its store (using keyword matching or semantic search) and returns relevant snippets as a `SearchMemoryResponse` containing a list of `MemoryResult` objects (each potentially holding events from a relevant past session).
7. **Agent Uses Results:** The tool returns these results to the agent, usually as part of the context or function response. The agent can then use this retrieved information to formulate its final answer to the user.

### Can an agent have access to more than one memory service?

* **Through Standard Configuration: No.** The framework (`adk web`, `adk api_server`) is designed to be configured with one single memory service at a time via the `--memory_service_uri` flag. This single service is then provided to the agent and accessed through the built-in `self.search_memory()` method. From a configuration standpoint, you can only choose one backend (`InMemory`, `VertexAiMemoryBankService`) for all agents served by that process.
* **Within Your Agent's Code: Yes, absolutely.** There is nothing preventing you from manually importing and instantiating another memory service directly inside your agent's code. This allows you to access multiple memory sources within a single agent turn.

For example, your agent could use the framework-configured `InMemoryMemoryService` to recall conversational history, and also manually instantiate a `VertexAiMemoryBankService` to look up information in a technical manual.

#### Example: Using Two Memory Services

Here’s how you could implement that in your agent’s code (illustrates the direct `search_memory(query)` call pattern):

> *Code examples: see [memory-python.md](memory-python.md), [memory-typescript.md](memory-typescript.md), [memory-go.md](memory-go.md), [memory-java.md](memory-java.md)*