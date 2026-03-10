# Memory Service — Python Examples

## 1. InMemoryMemoryService: add_session_to_memory, load_memory tool, two-runner cross-session recall

```python
import asyncio
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.memory import InMemoryMemoryService  # Import MemoryService
from google.adk.runners import Runner
from google.adk.tools import load_memory  # Tool to query memory
from google.genai.types import Content, Part

# --- Constants ---
APP_NAME = "memory_example_app"
USER_ID = "mem_user"
MODEL = "gemini-2.0-flash"

# --- Agent Definitions ---
# Agent 1: Simple agent to capture information
info_capture_agent = LlmAgent(
    model=MODEL,
    name="InfoCaptureAgent",
    instruction="Acknowledge the user's statement.",
)

# Agent 2: Agent that can use memory
memory_recall_agent = LlmAgent(
    model=MODEL,
    name="MemoryRecallAgent",
    instruction="Answer the user's question. Use the 'load_memory' tool "
                "if the answer might be in past conversations.",
    tools=[load_memory]  # Give the agent the tool
)

# --- Services ---
# Services must be shared across runners to share state and memory
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()  # Use in-memory for demo

async def run_scenario():
    # Turn 1: Capture some information in a session
    print("--- Turn 1: Capturing Information ---")
    runner1 = Runner(
        agent=info_capture_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service  # Provide the memory service to the Runner
    )
    session1_id = "session_info"
    await runner1.session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session1_id
    )
    user_input1 = Content(
        parts=[Part(text="My favorite project is Project Alpha.")], role="user"
    )

    final_response_text = "(No final response)"
    async for event in runner1.run_async(
        user_id=USER_ID, session_id=session1_id, new_message=user_input1
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response_text = event.content.parts[0].text
    print(f"Agent 1 Response: {final_response_text}")

    # Get the completed session and add it to memory
    completed_session1 = await runner1.session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session1_id
    )
    print("\n--- Adding Session 1 to Memory ---")
    await memory_service.add_session_to_memory(completed_session1)
    print("Session added to memory.")

    # Turn 2: Recall the information in a new session
    print("\n--- Turn 2: Recalling Information ---")
    runner2 = Runner(
        agent=memory_recall_agent,
        app_name=APP_NAME,
        session_service=session_service,  # Reuse the same service
        memory_service=memory_service     # Reuse the same service
    )
    session2_id = "session_recall"
    await runner2.session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session2_id
    )
    user_input2 = Content(
        parts=[Part(text="What is my favorite project?")], role="user"
    )

    final_response_text_2 = "(No final response)"
    async for event in runner2.run_async(
        user_id=USER_ID, session_id=session2_id, new_message=user_input2
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response_text_2 = event.content.parts[0].text
    print(f"Agent 2 Response: {final_response_text_2}")

# asyncio.run(run_scenario())
```

## 2. VertexAiMemoryBankService config + Runner wiring

```python
from google import adk
from google.adk.memory import VertexAiMemoryBankService

agent_engine_id = agent_engine.api_resource.name.split("/")[-1]

memory_service = VertexAiMemoryBankService(
    project="PROJECT_ID",
    location="LOCATION",
    agent_engine_id=agent_engine_id
)

runner = adk.Runner(
    ...
    memory_service=memory_service
)
```

## 3. PreloadMemoryTool in tools=[] + after_agent_callback auto-save pattern

```python
from google.adk.agents import Agent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

# PreloadMemoryTool: retrieves memory at the start of every turn
agent = Agent(
    model=MODEL_ID,
    name='weather_sentiment_agent',
    instruction="...",
    tools=[PreloadMemoryTool()]
)
```

```python
from google.adk.agents import Agent
from google import adk

async def auto_save_session_to_memory_callback(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session)

agent = Agent(
    model=MODEL,
    name="Generic_QA_Agent",
    instruction="Answer the user's questions",
    tools=[adk.tools.preload_memory_tool.PreloadMemoryTool()],
    after_agent_callback=auto_save_session_to_memory_callback,
)
```

## 4. Direct search_memory(query) call pattern — two memory services

```python
from google.adk.agents import Agent
from google.adk.memory import InMemoryMemoryService, VertexAiMemoryBankService
from google.genai import types

class MultiMemoryAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.memory_service = InMemoryMemoryService()
        # Manually instantiate a second memory service for document lookups
        self.vertexai_memorybank_service = VertexAiMemoryBankService(
            project="PROJECT_ID",
            location="LOCATION",
            agent_engine_id="AGENT_ENGINE_ID"
        )

    async def run(self, request: types.Content, **kwargs) -> types.Content:
        user_query = request.parts[0].text

        # 1. Search conversational history using the framework-provided memory
        conversation_context = await self.memory_service.search_memory(query=user_query)

        # 2. Search the document knowledge base using the manually created service
        document_context = await self.vertexai_memorybank_service.search_memory(
            query=user_query
        )

        # Combine context from both sources
        prompt = "From our past conversations, I remember:\n"
        prompt += f"{conversation_context.memories}\n\n"
        prompt += "From the technical manuals, I found:\n"
        prompt += f"{document_context.memories}\n\n"
        prompt += f"Based on all this, here is my answer to '{user_query}':"

        return await self.llm.generate_content_async(prompt)
```
