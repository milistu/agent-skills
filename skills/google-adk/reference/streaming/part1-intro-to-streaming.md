# Part 1: Introduction to ADK Gemini Live API Toolkit

Google's Agent Development Kit (ADK) provides a production-ready framework for building Bidi-streaming applications with Gemini models. This guide introduces ADK's streaming architecture, which enables real-time, two-way communication between users and AI agents through multimodal channels (text, audio, video).

**What you'll learn**: This part covers the fundamentals of Bidi-streaming, the underlying Live API technology (Gemini Live API and Vertex AI Live API), ADK's architectural components (`LiveRequestQueue`, `Runner`, `Agent`), and a complete FastAPI implementation example. You'll understand how ADK handles session management, tool orchestration, and platform abstraction—reducing months of infrastructure development to declarative configuration.

## ADK Gemini Live API Toolkit Demo

To help you understand the concepts in this guide, we provide a working demo application that showcases ADK bidirectional streaming in action. This FastAPI-based demo implements the complete streaming lifecycle with a practical, real-world architecture.

**Demo Repository**: [adk-samples/python/agents/bidi-demo](https://github.com/google/adk-samples/tree/main/python/agents/bidi-demo)

The demo features:

- **WebSocket Communication**: Real-time bidirectional streaming with concurrent upstream/downstream tasks
- **Multimodal Requests**: Text, audio, and image/video input with automatic transcription
- **Flexible Responses**: Text or audio output based on model capabilities
- **Interactive UI**: Web interface with event console for monitoring Live API events
- **Google Search Integration**: Agent equipped with tool calling capabilities

We strongly recommend installing and running this demo before diving into the guide. Hands-on experimentation will help you understand the concepts more deeply, and the demo code serves as a practical reference throughout all parts of this guide.

For installation instructions and usage details, see the [demo README](https://github.com/google/adk-samples/tree/main/python/agents/bidi-demo).

## 1.1 What is Bidi-streaming?

Bidi-streaming (Bidirectional streaming) represents a fundamental shift from traditional AI interactions. Instead of the rigid "ask-and-wait" pattern, it enables **real-time, two-way communication** where both human and AI can speak, listen, and respond simultaneously. This creates natural, human-like conversations with immediate responses and the revolutionary ability to interrupt ongoing interactions.

Think of the difference between sending emails and having a phone conversation. Traditional AI interactions are like emails—you send a complete message, wait for a complete response, then send another complete message. Bidi-streaming is like a phone conversation—fluid, natural, with the ability to interrupt, clarify, and respond in real-time.

### Key Characteristics

These characteristics distinguish Bidi-streaming from traditional AI interactions and make it uniquely powerful for creating engaging user experiences:

- **Two-way Communication**: Continuous data exchange without waiting for complete responses. Users can interrupt the AI mid-response with new input, creating a natural conversational flow. The AI responds after detecting the user has finished speaking (via automatic voice activity detection or explicit activity signals).
- **Responsive Interruption**: Perhaps the most important feature for the natural user experience—users can interrupt the agent mid-response with new input, just like in human conversation. If an AI is explaining quantum physics and you suddenly ask "wait, what's an electron?", the AI stops immediately and addresses your question.
- **Best for Multimodal**: Bidi-streaming excels at multimodal interactions because it can process different input types simultaneously through a single connection. Users can speak while showing documents, type follow-up questions during voice calls, or seamlessly switch between communication modes without losing context. This unified approach eliminates the complexity of managing separate channels for each modality.

### Difference from Other Streaming Types

Understanding how Bidi-streaming differs from other approaches is crucial for appreciating its unique value. The streaming landscape includes several distinct patterns, each serving different use cases:

**Bidi-streaming** differs fundamentally from other streaming approaches:

- **Server-Side Streaming**: One-way data flow from server to client. Like watching a live video stream—you receive continuous data but can't interact with it in real-time. Useful for dashboards or live feeds, but not for conversations.
- **Token-Level Streaming**: Sequential text token delivery without interruption. The AI generates response word-by-word, but you must wait for completion before sending new input. Like watching someone type a message in real-time—you see it forming, but can't interrupt.
- **Bidi-streaming**: Full two-way communication with interruption support. True conversational AI where both parties can speak, listen, and respond simultaneously. This is what enables natural dialogue where you can interrupt, clarify, or change topics mid-conversation.

## 1.2 Gemini Live API and Vertex AI Live API

ADK Gemini Live API Toolkit capabilities are powered by Live API technology, available through two platforms: **Gemini Live API** (via Google AI Studio) and **Vertex AI Live API** (via Google Cloud). Both provide real-time, low-latency streaming conversations with Gemini models, but serve different development and deployment needs.

Throughout this guide, we use **"Live API"** to refer to both platforms collectively, specifying "Gemini Live API" or "Vertex AI Live API" only when discussing platform-specific features or differences.

### What is the Live API?

Live API is Google's real-time conversational AI technology that enables **low-latency Bidi-streaming** with Gemini models. Unlike traditional request-response APIs, Live API establishes persistent WebSocket connections that support:

**Core Capabilities:**

- **Multimodal streaming**: Processes continuous streams of audio, video, and text in real-time
- **Voice Activity Detection (VAD)**: Automatically detects when users finish speaking, enabling natural turn-taking without explicit signals. The AI knows when to start responding and when to wait for more input
- **Immediate responses**: Delivers human-like spoken or text responses with minimal latency
- **Intelligent interruption**: Enables users to interrupt the AI mid-response, just like human conversations
- **Audio Transcription**: Real-time transcription of both user input and model output, enabling accessibility features and conversation logging without separate transcription services
- **Session Management**: Long conversations can span multiple connections through session resumption, with the API preserving full conversation history and context across reconnections
- **Tool Integration**: Function calling works seamlessly in streaming mode, with tools executing in the background while conversation continues

**Native Audio Model Features:**

- **Proactive Audio**: The model can initiate responses based on context awareness, creating more natural interactions where the AI offers help or clarification proactively (Native Audio models only)
- **Affective Dialog**: Advanced models understand tone of voice and emotional context, adapting responses to match the conversational mood and user sentiment (Native Audio models only)

For detailed information about Native Audio models and these features, see [Part 5: Audio/Images/Video](part5-audio-images-video.md).

**Technical Specifications:**

- **Audio input**: 16-bit PCM at 16kHz (mono)
- **Audio output**: 16-bit PCM at 24kHz (native audio models)
- **Video input**: 1 frame per second, recommended 768x768 resolution
- **Context windows**: Varies by model (typically 32k–128k tokens for Live API models)
- **Languages**: 24+ languages supported with automatic detection

### Gemini Live API vs Vertex AI Live API

Both APIs provide the same core Live API technology, but differ in deployment platform, authentication, and enterprise features:

| **Aspect** | **Gemini Live API** | **Vertex AI Live API** |
|---|---|---|
| **Access** | Google AI Studio | Google Cloud |
| **Authentication** | API key (`GOOGLE_API_KEY`) | Google Cloud credentials (`GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`) |
| **Best for** | Rapid prototyping, development, experimentation | Production deployments, enterprise applications |
| **Session Duration** | Audio-only: 15 min; Audio+video: 2 min; With context window compression: Unlimited | Both: 10 min; With context window compression: Unlimited |
| **Concurrent Sessions** | Tier-based quotas | Up to 1,000 per project (configurable via quota requests) |
| **Enterprise Features** | Basic | Advanced monitoring, logging, SLAs, session resumption (24h) |
| **Setup Complexity** | Minimal (API key only) | Requires Google Cloud project setup |
| **API Version** | `v1beta` | `v1beta1` |
| **API Endpoint** | `generativelanguage.googleapis.com` | `{location}-aiplatform.googleapis.com` |
| **Billing** | Usage tracked via API key | Google Cloud project billing |

**Concurrent session limits** are quota-based and may vary by account tier or configuration. Check your current quotas in Google AI Studio or Google Cloud Console.

## 1.3 ADK Gemini Live API Toolkit: For Building Realtime Agent Applications

Building realtime Agent applications from scratch presents significant engineering challenges. While Live API provides the underlying streaming technology, integrating it into production applications requires solving complex problems: managing WebSocket connections and reconnection logic, orchestrating tool execution and response handling, persisting conversation state across sessions, coordinating concurrent data flows for multimodal inputs, and handling platform differences between development and production environments.

ADK transforms these challenges into simple, declarative APIs. Instead of spending months building infrastructure for session management, tool orchestration, and state persistence, developers can focus on defining agent behavior and creating user experiences. This section explores what ADK handles automatically and why it's the recommended path for building production-ready streaming applications.

**Raw Live API vs. ADK Gemini Live API Toolkit:**

| Feature | Raw Live API (`google-genai` SDK) | ADK Gemini Live API Toolkit (`adk-python` and `adk-java` SDK) |
|---|---|---|
| **Agent Framework** | Not available | Single agent, multi-agent with sub-agents, sequential workflow agents, tool ecosystem, deployment ready, evaluation, security and more |
| **Tool Execution** | Manual tool execution and response handling | Automatic tool execution (see [Part 3: Event Handling](part3-event-handling.md)) |
| **Connection Management** | Manual reconnection and session resumption | Automatic reconnection and session resumption (see [Part 4: Run Configuration](part4-run-configuration.md)) |
| **Event Model** | Custom event structures and serialization | Unified event model with metadata (see [Part 3: Event Handling](part3-event-handling.md)) |
| **Async Event Processing Framework** | Manual async coordination and stream handling | `LiveRequestQueue`, `run_live()` async generator, automatic bidirectional flow coordination (see [Part 2: Sending Messages](part2-sending-messages.md) and [Part 3: Event Handling](part3-event-handling.md)) |
| **App-level Session Persistence** | Manual implementation | SQL databases (PostgreSQL, MySQL, SQLite), Vertex AI, in-memory |

### Platform Flexibility

One of ADK's most powerful features is its transparent support for both Gemini Live API and Vertex AI Live API. This platform flexibility enables a seamless development-to-production workflow: develop locally with Gemini API using free API keys, then deploy to production with Vertex AI using enterprise Google Cloud infrastructure—all **without changing application code**, only environment configuration.

#### How Platform Selection Works

ADK uses the `GOOGLE_GENAI_USE_VERTEXAI` environment variable to determine which Live API platform to use:

- `GOOGLE_GENAI_USE_VERTEXAI=FALSE` (or not set): Uses Gemini Live API via Google AI Studio
- `GOOGLE_GENAI_USE_VERTEXAI=TRUE`: Uses Vertex AI Live API via Google Cloud

This environment variable is read by the underlying `google-genai` SDK when ADK creates the LLM connection. No code changes are needed when switching platforms—only environment configuration changes.

**Development Phase (Gemini Live API / Google AI Studio)** benefits:

- Rapid prototyping with free API keys from Google AI Studio
- No Google Cloud setup required
- Instant experimentation with streaming features
- Zero infrastructure costs during development

**Production Phase (Vertex AI Live API / Google Cloud)** benefits:

- Enterprise-grade infrastructure via Google Cloud
- Advanced monitoring, logging, and cost controls
- Integration with existing Google Cloud services
- Production SLAs and support
- **No code changes required** — just environment configuration

By handling the complexity of session management, tool orchestration, state persistence, and platform differences, ADK lets you focus on building intelligent agent experiences rather than wrestling with streaming infrastructure.

## 1.4 ADK Gemini Live API Toolkit Architecture Overview

Now that you understand Live API technology and why ADK adds value, let's explore how ADK actually works. This section maps the complete data flow from your application through ADK's pipeline to Live API and back, showing which components handle which responsibilities.

You'll see how key components like `LiveRequestQueue`, `Runner`, and `Agent` orchestrate streaming conversations without requiring you to manage WebSocket connections, coordinate async flows, or handle platform-specific API differences.

### High-Level Architecture

The architecture separates concerns across three layers:

| Developer provides | ADK provides | Live API provides |
|---|---|---|
| **Web / Mobile** — Frontend applications that handle UI/UX, user input capture, and response display | **LiveRequestQueue** — Message queue that buffers and sequences incoming user messages (text content, audio blobs, control signals) for orderly processing by the agent | **Gemini Live API** (via Google AI Studio) and **Vertex AI Live API** (via Google Cloud) — Google's real-time language model services that process streaming input, generate responses, handle interruptions, support multimodal content, and provide advanced AI capabilities |
| **WebSocket / SSE Server** — Real-time communication server (e.g., FastAPI) that manages client connections, handles streaming protocols, and routes messages between clients and ADK | **Runner** — Execution engine that orchestrates agent sessions, manages conversation state, and provides the `run_live()` streaming interface | |
| **Agent** — Custom AI agent definition with specific instructions, tools, and behavior | **RunConfig** — Configuration for streaming behavior, modalities, and advanced features | |
| | **Internal components** (managed automatically): LLM Flow for the processing pipeline and GeminiLlmConnection for protocol translation | |

Data flows from the client through the transport layer into `LiveRequestQueue`, then through `Runner` → `Agent` → LLM Flow → `GeminiLlmConnection` → Live API. Responses travel the reverse path as yielded `Event` objects back to the client.

This architecture demonstrates ADK's clear separation of concerns: your application handles user interaction and transport protocols, ADK manages the streaming orchestration and state, and Live API provides the AI intelligence. By abstracting away the complexity of LLM-side streaming connection management, event loops, and protocol translation, ADK enables you to focus on building agent behavior and user experiences rather than streaming infrastructure.

## 1.5 ADK Gemini Live API Toolkit Application Lifecycle

ADK Gemini Live API Toolkit integrates Live API session into the ADK framework's application lifecycle. This integration creates a four-phase lifecycle that combines ADK's agent management with Live API's real-time streaming capabilities:

- **Phase 1: Application Initialization** (Once at Startup): Create an Agent, a SessionService, and a Runner
- **Phase 2: Session Initialization** (Once per User Session): Get or create an ADK Session, create a RunConfig, create a LiveRequestQueue, and start a `run_live()` event loop
- **Phase 3: Bidi-streaming with `run_live()` event loop** (One or More Times per User Session): Upstream sends messages via `LiveRequestQueue`; downstream receives agent `Event` objects
- **Phase 4: Terminate Live API session**: Call `LiveRequestQueue.close()`

In the following sections, each phase is detailed, showing exactly when to create each component and how they work together. Understanding this lifecycle pattern is essential for building robust streaming applications that can handle multiple concurrent sessions efficiently.

### Phase 1: Application Initialization

These components are created once when your application starts and shared across all streaming sessions. They define your agent's capabilities, manage conversation history, and orchestrate the streaming execution.

#### Define Your Agent

The `Agent` is the core of your streaming application—it defines what your AI can do, how it should behave, and which AI model powers it. You configure your agent with a specific model, tools it can use (like Google Search or custom APIs), and instructions that shape its personality and behavior.

The agent instance is **stateless and reusable**—you create it once and use it for all streaming sessions. Agent configuration is covered in the ADK Agent documentation.

For the latest supported models and their capabilities, see [Part 5: Audio/Images/Video](part5-audio-images-video.md).

`Agent` is the recommended shorthand for `LlmAgent` (both are imported from `google.adk.agents`). They are identical — use whichever you prefer. This guide uses `Agent` for brevity, but you may see `LlmAgent` in other ADK documentation and examples.

> *Code examples: see [part1-intro-to-streaming-python.md](part1-intro-to-streaming-python.md), [part1-intro-to-streaming-typescript.md](part1-intro-to-streaming-typescript.md), [part1-intro-to-streaming-go.md](part1-intro-to-streaming-go.md), [part1-intro-to-streaming-java.md](part1-intro-to-streaming-java.md)*

#### Define Your SessionService

The ADK Session manages conversation state and history across streaming sessions. It stores and retrieves session data, enabling features like conversation resumption and context persistence.

To create a `Session`, or get an existing one for a specified `session_id`, every ADK application needs a `SessionService`. For development purposes, ADK provides `InMemorySessionService` that loses session state when the application shuts down.

For production applications, choose a persistent session service based on your infrastructure:

**Use `DatabaseSessionService` if:**

- You need persistent storage with SQLite, PostgreSQL, or MySQL
- You're building single-server apps (SQLite) or multi-server deployments (PostgreSQL/MySQL)
- You want full control over data storage and backups
- Examples: `DatabaseSessionService(db_url="sqlite:///./sessions.db")` or `DatabaseSessionService(db_url="postgresql://user:pass@host/db")`

**Use `VertexAiSessionService` if:**

- You're already using Google Cloud Platform
- You want managed storage with built-in scalability
- You need tight integration with Vertex AI features
- Example: `VertexAiSessionService(project="my-project")`

Both provide session persistence capabilities—choose based on your infrastructure and scale requirements. See the ADK Session Management documentation for more details.

> *Code examples: see [part1-intro-to-streaming-python.md](part1-intro-to-streaming-python.md), [part1-intro-to-streaming-typescript.md](part1-intro-to-streaming-typescript.md), [part1-intro-to-streaming-go.md](part1-intro-to-streaming-go.md), [part1-intro-to-streaming-java.md](part1-intro-to-streaming-java.md)*

#### Define Your Runner

The Runner provides the runtime for the `Agent`. It manages the conversation flow, coordinates tool execution, handles events, and integrates with session storage. You create one runner instance at application startup and reuse it for all streaming sessions.

The `app_name` parameter is required and identifies your application in session storage. All sessions for your application are organized under this name.

> *Code examples: see [part1-intro-to-streaming-python.md](part1-intro-to-streaming-python.md), [part1-intro-to-streaming-typescript.md](part1-intro-to-streaming-typescript.md), [part1-intro-to-streaming-go.md](part1-intro-to-streaming-go.md), [part1-intro-to-streaming-java.md](part1-intro-to-streaming-java.md)*

### Phase 2: Session Initialization

#### Get or Create Session

ADK `Session` provides a "conversation thread" of the ADK Gemini Live API Toolkit application. Just like you wouldn't start every text message from scratch, agents need context regarding the ongoing interaction. `Session` is the ADK object designed specifically to track and manage these individual conversation threads.

##### ADK `Session` vs Live API session

ADK `Session` (managed by SessionService) provides **persistent conversation storage** across multiple Bidi-streaming sessions (can span hours, days, or even months), while Live API session (managed by Live API backend) is **a transient streaming context** that exists only during a single Bidi-streaming event loop (spans minutes or hours typically). When the loop starts, ADK initializes the Live API session with history from the ADK `Session`, then updates the ADK `Session` as new events occur.

For a detailed comparison with sequence diagrams, see [Part 4: Run Configuration](part4-run-configuration.md).

##### Session Identifiers Are Application-Defined

Sessions are identified by three parameters: `app_name`, `user_id`, and `session_id`. This three-level hierarchy enables multi-tenant applications where each user can have multiple concurrent sessions.

Both `user_id` and `session_id` are **arbitrary string identifiers** that you define based on your application's needs. ADK performs no format validation beyond `.strip()` on `session_id`:

- **`user_id` examples**: User UUIDs (`"550e8400-e29b-41d4-a716-446655440000"`), email addresses (`"alice@example.com"`), database IDs (`"user_12345"`), or simple identifiers (`"demo-user"`)
- **`session_id` examples**: Custom session tokens, UUIDs, timestamp-based IDs (`"session_2025-01-27_143022"`), or simple identifiers (`"demo-session"`)

**Auto-generation**: If you pass `session_id=None` or an empty string to `create_session()`, ADK automatically generates a UUID for you.

**Organizational hierarchy**: `app_name → user_id → session_id → Session`

This design enables scenarios like: multi-tenant applications where different users have isolated conversation spaces, single users with multiple concurrent chat threads (e.g., different topics), and per-device or per-browser session isolation.

##### Recommended Pattern: Get-or-Create

The recommended production pattern is to check if a session exists first, then create it only if needed. This approach safely handles both new sessions and conversation resumption. This pattern works correctly in all scenarios:

- **New conversations**: If the session doesn't exist, it's created automatically
- **Resuming conversations**: If the session already exists (e.g., reconnection after network interruption), the existing session is reused with full conversation history
- **Idempotent**: Safe to call multiple times without errors

**Important**: The session must exist before calling `runner.run_live()` with the same identifiers. If the session doesn't exist, `run_live()` will raise `ValueError: Session not found`.

> *Code examples: see [part1-intro-to-streaming-python.md](part1-intro-to-streaming-python.md), [part1-intro-to-streaming-typescript.md](part1-intro-to-streaming-typescript.md), [part1-intro-to-streaming-go.md](part1-intro-to-streaming-go.md), [part1-intro-to-streaming-java.md](part1-intro-to-streaming-java.md)*

#### Create RunConfig

[RunConfig](part4-run-configuration.md) defines the streaming behavior for this specific session—which modalities to use (text or audio), whether to enable transcription, voice activity detection, proactivity, and other advanced features.

`RunConfig` is **session-specific**—each streaming session can have different configuration. For example, one user might prefer text-only responses while another uses voice mode. See [Part 4: Run Configuration](part4-run-configuration.md) for complete configuration options.

> *Code examples: see [part1-intro-to-streaming-python.md](part1-intro-to-streaming-python.md), [part1-intro-to-streaming-typescript.md](part1-intro-to-streaming-typescript.md), [part1-intro-to-streaming-go.md](part1-intro-to-streaming-go.md), [part1-intro-to-streaming-java.md](part1-intro-to-streaming-java.md)*

#### Create LiveRequestQueue

`LiveRequestQueue` is the communication channel for sending messages to the agent during streaming. It's a thread-safe async queue that buffers user messages (text content, audio blobs, activity signals) for orderly processing.

`LiveRequestQueue` is **session-specific and stateful**—you create a new queue for each streaming session and close it when the session ends. Unlike `Agent` and `Runner`, queues cannot be reused across sessions.

**Never reuse a `LiveRequestQueue` across multiple streaming sessions.** Each call to `run_live()` requires a fresh queue. Reusing queues can cause message ordering issues and state corruption. The close signal persists in the queue and terminates the sender loop; reusing a queue would carry over this signal and any remaining messages from the previous session.

> *Code examples: see [part1-intro-to-streaming-python.md](part1-intro-to-streaming-python.md), [part1-intro-to-streaming-typescript.md](part1-intro-to-streaming-typescript.md), [part1-intro-to-streaming-go.md](part1-intro-to-streaming-go.md), [part1-intro-to-streaming-java.md](part1-intro-to-streaming-java.md)*

### Phase 3: Bidi-streaming with `run_live()` event loop

Once the streaming loop is running, you can send messages to the agent and receive responses **concurrently**—this is Bidi-streaming in action. The agent can be generating a response while you're sending new input, enabling natural interruption-based conversation.

#### Send Messages to the Agent

Use `LiveRequestQueue` methods to send different types of messages to the agent during the streaming session. The two primary methods are `send_content()` for structured text/content messages and `send_realtime()` for raw audio blobs. These methods are **non-blocking**—they immediately add messages to the queue without waiting for processing. This enables smooth, responsive user experiences even during heavy AI processing.

See [Part 2: Sending Messages](part2-sending-messages.md) for detailed API documentation.

> *Code examples: see [part1-intro-to-streaming-python.md](part1-intro-to-streaming-python.md), [part1-intro-to-streaming-typescript.md](part1-intro-to-streaming-typescript.md), [part1-intro-to-streaming-go.md](part1-intro-to-streaming-go.md), [part1-intro-to-streaming-java.md](part1-intro-to-streaming-java.md)*

#### Receive and Process Events

The `run_live()` async generator continuously yields `Event` objects as the agent processes input and generates responses. Each event represents a discrete occurrence—partial text generation, audio chunks, tool execution, transcription, interruption, or turn completion.

Events are designed for **streaming delivery**—you receive partial responses as they're generated, not just complete messages. This enables real-time UI updates and responsive user experiences.

See [Part 3: Event Handling](part3-event-handling.md) for comprehensive event handling patterns.

> *Code examples: see [part1-intro-to-streaming-python.md](part1-intro-to-streaming-python.md), [part1-intro-to-streaming-typescript.md](part1-intro-to-streaming-typescript.md), [part1-intro-to-streaming-go.md](part1-intro-to-streaming-go.md), [part1-intro-to-streaming-java.md](part1-intro-to-streaming-java.md)*

### Phase 4: Terminate Live API session

When the streaming session should end (user disconnects, conversation completes, timeout occurs), close the queue gracefully to signal termination.

#### Close the Queue

Calling `live_request_queue.close()` signals `run_live()` to stop yielding events and exit the async generator loop. The agent completes any in-progress processing and the streaming session ends cleanly.

> *Code examples: see [part1-intro-to-streaming-python.md](part1-intro-to-streaming-python.md), [part1-intro-to-streaming-typescript.md](part1-intro-to-streaming-typescript.md), [part1-intro-to-streaming-go.md](part1-intro-to-streaming-go.md), [part1-intro-to-streaming-java.md](part1-intro-to-streaming-java.md)*

### FastAPI Application Example

Here's a complete FastAPI WebSocket application showing all four phases integrated with proper Bidi-streaming. The key pattern is **upstream/downstream tasks**: the upstream task receives messages from WebSocket and sends them to `LiveRequestQueue`, while the downstream task receives `Event` objects from `run_live()` and sends them to the WebSocket.

For the production-ready implementation with full multimodal support (text, audio, image), see the complete [main.py](https://github.com/google/adk-samples/blob/31847c0723fbf16ddf6eed411eb070d1c76afd1a/python/agents/bidi-demo/app/main.py) file.

> *Code examples: see [part1-intro-to-streaming-python.md](part1-intro-to-streaming-python.md), [part1-intro-to-streaming-typescript.md](part1-intro-to-streaming-typescript.md), [part1-intro-to-streaming-go.md](part1-intro-to-streaming-go.md), [part1-intro-to-streaming-java.md](part1-intro-to-streaming-java.md)*

**Async Context Required**

All ADK bidirectional streaming applications **must run in an async context**. This requirement comes from multiple components:

- **`run_live()`**: ADK's streaming method is an async generator with no synchronous wrapper (unlike `run()`)
- **Session operations**: `get_session()` and `create_session()` are async methods
- **WebSocket operations**: FastAPI's `websocket.accept()`, `receive_text()`, and `send_text()` are all async
- **Concurrent tasks**: The upstream/downstream pattern requires `asyncio.gather()` for concurrent execution

### Key Concepts

**Upstream Task (WebSocket → LiveRequestQueue)**

The upstream task continuously receives messages from the WebSocket client and forwards them to the `LiveRequestQueue`. This enables the user to send messages to the agent at any time, even while the agent is generating a response.

**Downstream Task (run_live() → WebSocket)**

The downstream task continuously receives `Event` objects from `run_live()` and sends them to the WebSocket client. This streams the agent's responses, tool executions, transcriptions, and other events to the user in real-time.

**Concurrent Execution with Cleanup**

Both tasks run concurrently using `asyncio.gather()`, enabling true Bidi-streaming. The `try/finally` block ensures `LiveRequestQueue.close()` is called even if exceptions occur, minimizing session resource usage.

This pattern—concurrent upstream/downstream tasks with guaranteed cleanup—is the foundation of production-ready streaming applications. The lifecycle pattern (initialize once, stream many times) enables efficient resource usage and clean separation of concerns, with application components remaining stateless and reusable while session-specific state is isolated in `LiveRequestQueue`, `RunConfig`, and session records.

#### Production Considerations

For production applications, consider:

- **Error handling (ADK)**: Add proper error handling for ADK streaming events. See [Part 3: Event Handling](part3-event-handling.md) for details on error event handling. Handle task cancellation gracefully by catching `asyncio.CancelledError` during shutdown. Check exceptions from `asyncio.gather()` with `return_exceptions=True`—exceptions don't propagate automatically.
- **Error handling (Web)**: Handle web application-specific errors in upstream/downstream tasks. For example, with FastAPI catch `WebSocketDisconnect` (client disconnected), `ConnectionClosedError` (connection lost), and `RuntimeError` (sending to closed connection). Validate WebSocket connection state before sending with `websocket.client_state`.
- **Authentication and authorization**: Implement authentication and authorization for your endpoints.
- **Rate limiting and quotas**: Add rate limiting and timeout controls. For guidance on concurrent sessions and quota management, see [Part 4: Run Configuration](part4-run-configuration.md).
- **Structured logging**: Use structured logging for debugging.
- **Persistent session services**: Consider using `DatabaseSessionService` or `VertexAiSessionService`. See the ADK Session Services documentation for more details.

## 1.6 What We Will Learn

This guide takes you through ADK Gemini Live API Toolkit's architecture step by step, following the natural flow of streaming applications: how messages travel upstream from users to agents, how events flow downstream from agents to users, how to configure session behaviors, and how to implement multimodal features. Each part focuses on a specific component of the streaming architecture with practical patterns you can apply immediately:

- **[Part 2: Sending Messages](part2-sending-messages.md)** — Learn how ADK's `LiveRequestQueue` provides a unified interface for handling text, audio, and control messages. You'll understand the `LiveRequest` message model, how to send different types of content, manage user activity signals, and handle graceful session termination through a single, elegant API.
- **[Part 3: Event Handling](part3-event-handling.md)** — Master event handling in ADK's streaming architecture. Learn how to process different event types (text, audio, transcriptions, tool calls), manage conversation flow with interruption and turn completion signals, serialize events for network transport, and leverage ADK's automatic tool execution.
- **[Part 4: Run Configuration](part4-run-configuration.md)** — Configure sophisticated streaming behaviors including multimodal interactions, intelligent proactivity, session resumption, and cost controls. Learn which features are available on different models and how to declaratively control your streaming sessions through RunConfig.
- **[Part 5: Audio/Images/Video](part5-audio-images-video.md)** — Implement voice and video features with ADK's multimodal capabilities. Understand audio specifications, streaming architectures, voice activity detection, audio transcription, and best practices for building natural voice-enabled AI experiences.

### Prerequisites and Learning Resources

For building an ADK Gemini Live API Toolkit application in production, we recommend having basic knowledge of the following technologies:

**ADK (Agent Development Kit)** — Google's production-ready framework for building AI agents with streaming capabilities. ADK provides high-level abstractions for session management, tool orchestration, and state persistence, eliminating the need to implement low-level streaming infrastructure from scratch.

**Live API (Gemini Live API and Vertex AI Live API)** — Google's real-time conversational AI technology that enables low-latency bidirectional streaming with Gemini models. The Live API provides the underlying WebSocket-based protocol that powers ADK's streaming capabilities, handling multimodal input/output and natural conversation flow.

**Python Async Programming** — Python's built-in support for asynchronous programming using `async`/`await` syntax and the `asyncio` library. ADK streaming is built on async generators and coroutines, requiring familiarity with concepts like async functions, awaiting tasks, and concurrent execution with `asyncio.gather()`.

**Pydantic** — A Python library for data validation and settings management using Python type annotations. ADK uses Pydantic models extensively for structured data (like `Event`, `RunConfig`, and `Content`), providing type safety, automatic validation, and JSON serialization via `.model_dump_json()`.

**FastAPI** — A modern, high-performance Python web framework for building APIs with automatic OpenAPI documentation. FastAPI's native support for WebSockets and async request handling makes it ideal for building ADK streaming endpoints. FastAPI is included in the `adk-python` package and used by ADK's `adk web` tool for rapid prototyping. Alternative frameworks with WebSocket support (like Flask-SocketIO or Starlette) can also be used.

**WebSockets** — A protocol providing full-duplex (two-way) communication channels over a single TCP connection. WebSockets enable real-time bidirectional data flow between clients and servers, making them the standard transport for streaming applications. Unlike HTTP request-response, WebSocket connections persist, allowing both parties to send messages at any time.

**SSE (Server-Sent Events)** — A standard for servers to push data to web clients over HTTP. Unlike WebSockets, SSE is unidirectional (server-to-client only), making it simpler but less flexible. SSE is useful for streaming agent responses when you don't need client-to-server streaming, such as when user input comes through separate HTTP POST requests.

While this guide covers ADK-specific concepts thoroughly, familiarity with these underlying technologies will help you build more robust production applications.

## Summary

In this introduction, you learned how ADK transforms complex real-time streaming infrastructure into a developer-friendly framework. We covered the fundamentals of Live API's bidirectional streaming capabilities, examined how ADK simplifies the streaming complexity through abstractions like `LiveRequestQueue`, `Runner`, and `run_live()`, and explored the complete application lifecycle from initialization through session termination. You now understand how ADK handles the heavy lifting—LLM-side streaming connection management, state persistence, platform differences, and event coordination—so you can focus on building intelligent agent experiences. With this foundation in place, you're ready to dive into the specifics of sending messages, handling events, configuring sessions, and implementing multimodal features in the following parts.

---

Next: [Part 2: Sending Messages](part2-sending-messages.md)
