# Session State — Python Examples

## 1. `{key}` Templating in `LlmAgent` Instructions

Inject session state values directly into an agent's instruction string using `{key}` placeholders.

```python
from google.adk.agents import LlmAgent

story_generator = LlmAgent(
    name="StoryGenerator",
    model="gemini-2.0-flash",
    instruction="Write a short story about a cat, focusing on the theme: {topic}."
)

# Assuming session.state['topic'] is set to "friendship", the LLM
# will receive the following instruction:
# "Write a short story about a cat, focusing on the theme: friendship."

# Use {topic?} for an optional key that may not be present:
optional_generator = LlmAgent(
    name="OptionalStoryGenerator",
    model="gemini-2.0-flash",
    instruction="Write a short story about a cat, focusing on the theme: {topic?}."
)
```

## 2. `InstructionProvider` Function — Literal Curly Braces

When instructions contain literal curly braces (e.g., JSON examples), use an `InstructionProvider`
function instead of a string. The ADK will not attempt state injection; the string is passed as-is.

```python
from google.adk.agents import LlmAgent
from google.adk.agents.readonly_context import ReadonlyContext

# This is an InstructionProvider
def my_instruction_provider(context: ReadonlyContext) -> str:
    # No state injection occurs — curly braces are treated as literal text.
    return 'Format your output as JSON: {"city": "<name>", "population": <number>}'

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="template_helper_agent",
    instruction=my_instruction_provider
)
```

## 3. `inject_session_state` Utility with `InstructionProvider`

Use `inject_session_state` when you need both an `InstructionProvider` and selective state injection.
Only `{key}` placeholders matching valid state variable names are replaced; other braces are left alone.

```python
from google.adk.agents import LlmAgent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.utils import instructions_utils

async def my_dynamic_instruction_provider(context: ReadonlyContext) -> str:
    template = "This is a {adjective} instruction. Use JSON like: {\"key\": \"value\"}."
    # Injects the 'adjective' state variable.
    # The JSON braces are left alone because their content is not a valid identifier.
    return await instructions_utils.inject_session_state(template, context)

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="dynamic_template_helper_agent",
    instruction=my_dynamic_instruction_provider
)
```

## 4. `output_key` → `get_session()` → `state.get()` Round-Trip

The simplest way to persist an agent's text response into state. The `Runner` uses `output_key`
to create the `EventActions.state_delta` automatically via `append_event`.

```python
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai.types import Content, Part

# Define agent with output_key
greeting_agent = LlmAgent(
    name="Greeter",
    model="gemini-2.0-flash",
    instruction="Generate a short, friendly greeting.",
    output_key="last_greeting"  # Saves final response text to state['last_greeting']
)

# --- Setup Runner and Session ---
app_name, user_id, session_id = "state_app", "user1", "session1"
session_service = InMemorySessionService()
runner = Runner(
    agent=greeting_agent,
    app_name=app_name,
    session_service=session_service
)
session = await session_service.create_session(
    app_name=app_name,
    user_id=user_id,
    session_id=session_id
)
print(f"Initial state: {session.state}")

# --- Run the Agent ---
user_message = Content(parts=[Part(text="Hello")])
for event in runner.run(user_id=user_id, session_id=session_id, new_message=user_message):
    if event.is_final_response():
        print("Agent responded.")  # Response text is also in event.content

# --- Check Updated State ---
updated_session = await session_service.get_session(
    app_name=app_name, user_id=user_id, session_id=session_id
)
print(f"State after agent run: {updated_session.state}")
# Expected: {'last_greeting': 'Hello there! How can I help you today?'}
greeting = updated_session.state.get("last_greeting")
print(f"Saved greeting: {greeting}")
```

## 5. `EventActions.state_delta` — Manual State Update via `append_event`

For complex updates: multiple keys, non-string values, scoped prefixes (`user:`, `app:`, `temp:`),
or updates not tied to an agent's final text response.

```python
from google.adk.sessions import InMemorySessionService
from google.adk.events import Event, EventActions
from google.genai.types import Content
import time

# --- Setup ---
session_service = InMemorySessionService()
app_name, user_id, session_id = "state_app_manual", "user2", "session2"
session = await session_service.create_session(
    app_name=app_name,
    user_id=user_id,
    session_id=session_id,
    state={"user:login_count": 0, "task_status": "idle"}
)
print(f"Initial state: {session.state}")

# --- Define State Changes ---
current_time = time.time()
state_changes = {
    "task_status": "active",                                           # session-scoped
    "user:login_count": session.state.get("user:login_count", 0) + 1, # user-scoped
    "user:last_login_ts": current_time,                                # user-scoped
    "temp:validation_needed": True                                     # temp (discarded after invocation)
}

# --- Create Event with Actions ---
actions_with_update = EventActions(state_delta=state_changes)
system_event = Event(
    invocation_id="inv_login_update",
    author="system",
    actions=actions_with_update,
    timestamp=current_time
)

# --- Append the Event (this updates the state) ---
await session_service.append_event(session, system_event)
print("`append_event` called with explicit state delta.")

# --- Check Updated State ---
updated_session = await session_service.get_session(
    app_name=app_name, user_id=user_id, session_id=session_id
)
print(f"State after event: {updated_session.state}")
# Expected: {'user:login_count': 1, 'task_status': 'active', 'user:last_login_ts': <timestamp>}
# Note: 'temp:validation_needed' is NOT present (discarded after invocation).
```

## 6. `CallbackContext` / `ToolContext` State Mutation

The recommended way to mutate state from within callbacks or tool functions. Changes made to
`context.state` are automatically captured into the event's `state_delta`.

```python
from google.adk.agents import CallbackContext  # or ToolContext for tools

def my_callback_or_tool_function(
    context: CallbackContext,  # Or ToolContext
    # ... other parameters ...
):
    # Read then update an existing state value
    count = context.state.get("user_action_count", 0)
    context.state["user_action_count"] = count + 1

    # Add a temporary value (discarded after the invocation ends)
    context.state["temp:last_operation_status"] = "success"

    # Changes are automatically part of the event's state_delta —
    # no manual EventActions construction needed.
    # ... rest of callback/tool logic ...
```
