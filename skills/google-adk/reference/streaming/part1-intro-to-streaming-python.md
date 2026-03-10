# Streaming Part 1 — Python Examples

Source: [Part 1: Introduction to ADK Gemini Live API Toolkit](part1-intro-to-streaming.md)

---

## Phase 1: Define Your Agent

Agent definition with a model and tools. The agent is stateless and reusable across all sessions.

Demo: [agent.py:10-15](https://github.com/google/adk-samples/blob/31847c0723fbf16ddf6eed411eb070d1c76afd1a/python/agents/bidi-demo/app/google_search_agent/agent.py#L10-L15)

```python
"""Google Search Agent definition for ADK Gemini Live API Toolkit demo."""

import os
from google.adk.agents import Agent
from google.adk.tools import google_search

# Default models for Live API with native audio support:
# - Gemini Live API: gemini-2.5-flash-native-audio-preview-12-2025
# - Vertex AI Live API: gemini-live-2.5-flash-native-audio
agent = Agent(
    name="google_search_agent",
    model=os.getenv("DEMO_AGENT_MODEL", "gemini-2.5-flash-native-audio-preview-12-2025"),
    tools=[google_search],
    instruction="You are a helpful assistant that can search the web."
)
```

---

## Phase 1: Define Your SessionService

Create an in-memory session service for development. For production use `DatabaseSessionService` or `VertexAiSessionService`.

Demo: [main.py:37](https://github.com/google/adk-samples/blob/31847c0723fbf16ddf6eed411eb070d1c76afd1a/python/agents/bidi-demo/app/main.py#L37)

```python
from google.adk.sessions import InMemorySessionService

# Define your session service
session_service = InMemorySessionService()
```

---

## Phase 1: Define Your Runner

Create the runner once at startup and reuse across all sessions. `app_name` organises all sessions for this application.

Demo: [main.py:50,53](https://github.com/google/adk-samples/blob/31847c0723fbf16ddf6eed411eb070d1c76afd1a/python/agents/bidi-demo/app/main.py#L50)

```python
from google.adk.runners import Runner

APP_NAME = "bidi-demo"

# Define your runner
runner = Runner(
    app_name=APP_NAME,
    agent=agent,
    session_service=session_service
)
```

---

## Phase 2: Get or Create Session

Get-or-create pattern for safe handling of both new sessions and reconnections.

Demo: [main.py:155-161](https://github.com/google/adk-samples/blob/31847c0723fbf16ddf6eed411eb070d1c76afd1a/python/agents/bidi-demo/app/main.py#L155-L161)

```python
# Get or create session (handles both new sessions and reconnections)
session = await session_service.get_session(
    app_name=APP_NAME,
    user_id=user_id,
    session_id=session_id
)
if not session:
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )
```

---

## Phase 2: Create RunConfig

Configure streaming mode, response modalities, audio transcription, and session resumption.

Demo: [main.py:110-124](https://github.com/google/adk-samples/blob/31847c0723fbf16ddf6eed411eb070d1c76afd1a/python/agents/bidi-demo/app/main.py#L110-L124)

```python
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.genai import types

# Native audio models require AUDIO response modality with audio transcription
response_modalities = ["AUDIO"]
run_config = RunConfig(
    streaming_mode=StreamingMode.BIDI,
    response_modalities=response_modalities,
    input_audio_transcription=types.AudioTranscriptionConfig(),
    output_audio_transcription=types.AudioTranscriptionConfig(),
    session_resumption=types.SessionResumptionConfig()
)
```

---

## Phase 2: Create LiveRequestQueue

Create a fresh queue per session. Never reuse across sessions.

Demo: [main.py:163](https://github.com/google/adk-samples/blob/31847c0723fbf16ddf6eed411eb070d1c76afd1a/python/agents/bidi-demo/app/main.py#L163)

```python
from google.adk.agents.live_request_queue import LiveRequestQueue

live_request_queue = LiveRequestQueue()
```

---

## Phase 3: Send Messages via LiveRequestQueue

`send_content()` for text, `send_realtime()` for audio blobs. Both are non-blocking.

Demo: [main.py:169-217](https://github.com/google/adk-samples/blob/31847c0723fbf16ddf6eed411eb070d1c76afd1a/python/agents/bidi-demo/app/main.py#L169-L217)

```python
from google.genai import types

# Send text content
content = types.Content(parts=[types.Part(text=json_message["text"])])
live_request_queue.send_content(content)

# Send audio blob
audio_blob = types.Blob(
    mime_type="audio/pcm;rate=16000",
    data=audio_data
)
live_request_queue.send_realtime(audio_blob)
```

---

## Phase 3: Consume Events from run_live()

Async generator that yields `Event` objects as they are produced. Each event is serialisable to JSON.

Demo: [main.py:219-234](https://github.com/google/adk-samples/blob/31847c0723fbf16ddf6eed411eb070d1c76afd1a/python/agents/bidi-demo/app/main.py#L219-L234)

```python
async for event in runner.run_live(
    user_id=user_id,
    session_id=session_id,
    live_request_queue=live_request_queue,
    run_config=run_config
):
    event_json = event.model_dump_json(exclude_none=True, by_alias=True)
    await websocket.send_text(event_json)
```

---

## Phase 4: Close the Queue

Signal `run_live()` to exit by closing the queue. Always call in a `finally` block.

Demo: [main.py:253](https://github.com/google/adk-samples/blob/31847c0723fbf16ddf6eed411eb070d1c76afd1a/python/agents/bidi-demo/app/main.py#L253)

```python
live_request_queue.close()
```

---

## Complete FastAPI WebSocket Example

Full integration of all four lifecycle phases in a single FastAPI endpoint. The upstream task feeds user messages into the queue while the downstream task drains events back to the client—both run concurrently via `asyncio.gather()`. This is the crown-jewel pattern for production ADK streaming applications.

Demo: [main.py (full file)](https://github.com/google/adk-samples/blob/31847c0723fbf16ddf6eed411eb070d1c76afd1a/python/agents/bidi-demo/app/main.py)

```python
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from google.adk.runners import Runner
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.agents.live_request_queue import LiveRequestQueue
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google_search_agent.agent import agent

# ========================================
# Phase 1: Application Initialization (once at startup)
# ========================================

APP_NAME = "bidi-demo"

app = FastAPI()

# Define your session service
session_service = InMemorySessionService()

# Define your runner
runner = Runner(
    app_name=APP_NAME,
    agent=agent,
    session_service=session_service
)

# ========================================
# WebSocket Endpoint
# ========================================

@app.websocket("/ws/{user_id}/{session_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, session_id: str) -> None:
    await websocket.accept()

    # ========================================
    # Phase 2: Session Initialization (once per streaming session)
    # ========================================

    # Create RunConfig
    response_modalities = ["AUDIO"]
    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        response_modalities=response_modalities,
        input_audio_transcription=types.AudioTranscriptionConfig(),
        output_audio_transcription=types.AudioTranscriptionConfig(),
        session_resumption=types.SessionResumptionConfig()
    )

    # Get or create session
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )
    if not session:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )

    # Create LiveRequestQueue
    live_request_queue = LiveRequestQueue()

    # ========================================
    # Phase 3: Active Session (concurrent bidirectional communication)
    # ========================================

    async def upstream_task() -> None:
        """Receives messages from WebSocket and sends to LiveRequestQueue."""
        try:
            while True:
                # Receive text message from WebSocket
                data: str = await websocket.receive_text()

                # Send to LiveRequestQueue
                content = types.Content(parts=[types.Part(text=data)])
                live_request_queue.send_content(content)
        except WebSocketDisconnect:
            # Client disconnected - signal queue to close
            pass

    async def downstream_task() -> None:
        """Receives Events from run_live() and sends to WebSocket."""
        async for event in runner.run_live(
            user_id=user_id,
            session_id=session_id,
            live_request_queue=live_request_queue,
            run_config=run_config
        ):
            # Send event as JSON to WebSocket
            await websocket.send_text(
                event.model_dump_json(exclude_none=True, by_alias=True)
            )

    # Run both tasks concurrently
    try:
        await asyncio.gather(
            upstream_task(),
            downstream_task(),
            return_exceptions=True
        )
    finally:
        # ========================================
        # Phase 4: Session Termination
        # ========================================

        # Always close the queue, even if exceptions occurred
        live_request_queue.close()
```
