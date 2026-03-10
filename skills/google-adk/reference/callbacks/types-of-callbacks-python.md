# Callback Types — Python Examples

## before_agent_callback

Checks `skip_llm_agent` in session state. Returns `Content` to skip the agent, or `None` to proceed.

```python
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import InMemoryRunner
from google.genai import types
from typing import Optional

GEMINI_2_FLASH = "gemini-2.0-flash"

def check_if_agent_should_run(callback_context: CallbackContext) -> Optional[types.Content]:
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Callback] Entering agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback] Current State: {current_state}")

    if current_state.get("skip_llm_agent", False):
        print(f"[Callback] State condition 'skip_llm_agent=True' met: Skipping agent {agent_name}.")
        return types.Content(
            parts=[types.Part(text=f"Agent {agent_name} skipped by before_agent_callback due to state.")],
            role="model"
        )
    else:
        print(f"[Callback] State condition not met: Proceeding with agent {agent_name}.")
        return None

llm_agent_with_before_cb = LlmAgent(
    name="MyControlledAgent",
    model=GEMINI_2_FLASH,
    instruction="You are a concise assistant.",
    description="An LLM agent demonstrating stateful before_agent_callback",
    before_agent_callback=check_if_agent_should_run
)

async def main():
    app_name = "before_agent_demo"
    user_id = "test_user"
    session_id_run = "session_will_run"
    session_id_skip = "session_will_skip"

    runner = InMemoryRunner(agent=llm_agent_with_before_cb, app_name=app_name)
    session_service = runner.session_service

    session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id_run)
    session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id_skip,
        state={"skip_llm_agent": True}
    )

    # Scenario 1: callback allows agent execution
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id_run,
        new_message=types.Content(role="user", parts=[types.Part(text="Hello, please respond.")])
    ):
        if event.is_final_response() and event.content:
            print(f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}")

    # Scenario 2: callback intercepts and skips agent
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id_skip,
        new_message=types.Content(role="user", parts=[types.Part(text="This message won't reach the LLM.")])
    ):
        if event.is_final_response() and event.content:
            print(f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}")

await main()
```

## after_agent_callback

Checks `add_concluding_note` in session state. Returns replacement `Content` or `None` to pass through the agent's original output.

```python
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import InMemoryRunner
from google.genai import types
from typing import Optional

GEMINI_2_FLASH = "gemini-2.0-flash"

def modify_output_after_agent(callback_context: CallbackContext) -> Optional[types.Content]:
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Callback] Exiting agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback] Current State: {current_state}")

    if current_state.get("add_concluding_note", False):
        print(f"[Callback] State condition 'add_concluding_note=True' met: Replacing agent {agent_name}'s output.")
        return types.Content(
            parts=[types.Part(text="Concluding note added by after_agent_callback, replacing original output.")],
            role="model"
        )
    else:
        print(f"[Callback] State condition not met: Using agent {agent_name}'s original output.")
        return None

llm_agent_with_after_cb = LlmAgent(
    name="MySimpleAgentWithAfter",
    model=GEMINI_2_FLASH,
    instruction="You are a simple agent. Just say 'Processing complete!'",
    description="An LLM agent demonstrating after_agent_callback for output modification",
    after_agent_callback=modify_output_after_agent
)

async def main():
    app_name = "after_agent_demo"
    user_id = "test_user_after"
    session_id_normal = "session_run_normally"
    session_id_modify = "session_modify_output"

    runner = InMemoryRunner(agent=llm_agent_with_after_cb, app_name=app_name)
    session_service = runner.session_service

    session_service.create_session(app_name=app_name, user_id=user_id, session_id=session_id_normal)
    session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id_modify,
        state={"add_concluding_note": True}
    )

    # Scenario 1: original output is used
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id_normal,
        new_message=types.Content(role="user", parts=[types.Part(text="Process this please.")])
    ):
        if event.is_final_response() and event.content:
            print(f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}")

    # Scenario 2: callback replaces the agent's output
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id_modify,
        new_message=types.Content(role="user", parts=[types.Part(text="Process this and add note.")])
    ):
        if event.is_final_response() and event.content:
            print(f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}")

await main()
```

## before_model_callback

Mutates `llm_request.config.system_instruction` and returns an `LlmResponse` to block the LLM call when "BLOCK" appears in the user message, or `None` to proceed.

```python
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from typing import Optional

GEMINI_2_FLASH = "gemini-2.0-flash"

def simple_before_model_modifier(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    print(f"[Callback] Before model call for agent: {agent_name}")

    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == "user":
        if llm_request.contents[-1].parts:
            last_user_message = llm_request.contents[-1].parts[0].text
    print(f"[Callback] Inspecting last user message: '{last_user_message}'")

    # Modification: prefix the system instruction
    original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[])
    prefix = "[Modified by Callback] "
    if not isinstance(original_instruction, types.Content):
        original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])
    if not original_instruction.parts:
        original_instruction.parts.append(types.Part(text=""))
    modified_text = prefix + (original_instruction.parts[0].text or "")
    original_instruction.parts[0].text = modified_text
    llm_request.config.system_instruction = original_instruction
    print(f"[Callback] Modified system instruction to: '{modified_text}'")

    # Skip: block if user message contains "BLOCK"
    if "BLOCK" in last_user_message.upper():
        print("[Callback] 'BLOCK' keyword found. Skipping LLM call.")
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="LLM call was blocked by before_model_callback.")],
            )
        )
    print("[Callback] Proceeding with LLM call.")
    return None

my_llm_agent = LlmAgent(
    name="ModelCallbackAgent",
    model=GEMINI_2_FLASH,
    instruction="You are a helpful assistant.",
    description="An LLM agent demonstrating before_model_callback",
    before_model_callback=simple_before_model_modifier
)

APP_NAME = "guardrail_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=my_llm_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

async def call_agent_async(query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            print("Agent Response: ", event.content.parts[0].text)

await call_agent_async("write a joke on BLOCK")
```

## after_model_callback

Inspects the LLM response text and replaces occurrences of "joke" with "funny story". Returns a new `LlmResponse` on modification, or `None` to pass through unchanged.

```python
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from copy import deepcopy
from typing import Optional

GEMINI_2_FLASH = "gemini-2.0-flash"

def simple_after_model_modifier(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    print(f"[Callback] After model call for agent: {agent_name}")

    original_text = ""
    if llm_response.content and llm_response.content.parts:
        if llm_response.content.parts[0].text:
            original_text = llm_response.content.parts[0].text
            print(f"[Callback] Inspected original response text: '{original_text[:100]}...'")
        elif llm_response.content.parts[0].function_call:
            print(f"[Callback] Response contains function call. No text modification.")
            return None
        else:
            print("[Callback] No text content found.")
            return None
    elif llm_response.error_message:
        print(f"[Callback] Response contains error. No modification.")
        return None
    else:
        return None

    search_term = "joke"
    replace_term = "funny story"
    if search_term in original_text.lower():
        print(f"[Callback] Found '{search_term}'. Modifying response.")
        modified_text = original_text.replace(search_term, replace_term)
        modified_text = modified_text.replace(search_term.capitalize(), replace_term.capitalize())
        modified_parts = [deepcopy(part) for part in llm_response.content.parts]
        modified_parts[0].text = modified_text
        return LlmResponse(
            content=types.Content(role="model", parts=modified_parts),
            grounding_metadata=llm_response.grounding_metadata
        )
    else:
        print(f"[Callback] '{search_term}' not found. Passing original response through.")
        return None

my_llm_agent = LlmAgent(
    name="AfterModelCallbackAgent",
    model=GEMINI_2_FLASH,
    instruction="You are a helpful assistant.",
    description="An LLM agent demonstrating after_model_callback",
    after_model_callback=simple_after_model_modifier
)

APP_NAME = "guardrail_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=my_llm_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

async def call_agent_async(query):
    session, runner = await setup_session_and_runner()
    content = types.Content(role="user", parts=[types.Part(text=query)])
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            print("Agent Response: ", event.content.parts[0].text)

await call_agent_async('write multiple times the word "joke"')
```

## before_tool_callback

Modifies tool `args` (redirects "Canada" to "France") or returns a result dict to skip tool execution entirely when "BLOCK" is passed.

```python
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from google.genai import types
from typing import Optional, Dict, Any

GEMINI_2_FLASH = "gemini-2.0-flash"

def get_capital_city(country: str) -> str:
    """Retrieves the capital city of a given country."""
    print(f"--- Tool 'get_capital_city' executing with country: {country} ---")
    country_capitals = {
        "united states": "Washington, D.C.",
        "canada": "Ottawa",
        "france": "Paris",
        "germany": "Berlin",
    }
    return country_capitals.get(country.lower(), f"Capital not found for {country}")

capital_tool = FunctionTool(func=get_capital_city)

def simple_before_tool_modifier(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    print(f"[Callback] Original args: {args}")

    if tool_name == "get_capital_city" and args.get("country", "").lower() == "canada":
        print("[Callback] Detected 'Canada'. Modifying args to 'France'.")
        args["country"] = "France"
        return None  # proceed with modified args

    if tool_name == "get_capital_city" and args.get("country", "").upper() == "BLOCK":
        print("[Callback] Detected 'BLOCK'. Skipping tool execution.")
        return {"result": "Tool execution was blocked by before_tool_callback."}

    print("[Callback] Proceeding with original or previously modified args.")
    return None

my_llm_agent = LlmAgent(
    name="ToolCallbackAgent",
    model=GEMINI_2_FLASH,
    instruction="You are an agent that can find capital cities. Use the get_capital_city tool.",
    description="An LLM agent demonstrating before_tool_callback",
    tools=[capital_tool],
    before_tool_callback=simple_before_tool_modifier
)

APP_NAME = "guardrail_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=my_llm_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

async def call_agent_async(query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            print("Agent Response: ", event.content.parts[0].text)

await call_agent_async("Canada")
```

## after_tool_callback

Inspects the tool result dict and appends a note when the capital is "Washington, D.C.". Returns the modified dict or `None` to pass through the original.

```python
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from google.genai import types
from copy import deepcopy
from typing import Optional, Dict, Any

GEMINI_2_FLASH = "gemini-2.0-flash"

def get_capital_city(country: str) -> dict:
    """Retrieves the capital city of a given country."""
    print(f"--- Tool 'get_capital_city' executing with country: {country} ---")
    country_capitals = {
        "united states": "Washington, D.C.",
        "canada": "Ottawa",
        "france": "Paris",
        "germany": "Berlin",
    }
    return {"result": country_capitals.get(country.lower(), f"Capital not found for {country}")}

capital_tool = FunctionTool(func=get_capital_city)

def simple_after_tool_modifier(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"[Callback] After tool call for tool '{tool_name}' in agent '{agent_name}'")
    print(f"[Callback] Args used: {args}")
    print(f"[Callback] Original tool_response: {tool_response}")

    original_result_value = tool_response.get("result", "")

    if tool_name == "get_capital_city" and original_result_value == "Washington, D.C.":
        print("[Callback] Detected 'Washington, D.C.'. Modifying tool response.")
        modified_response = deepcopy(tool_response)
        modified_response["result"] = f"{original_result_value} (Note: This is the capital of the USA)."
        modified_response["note_added_by_callback"] = True
        print(f"[Callback] Modified tool_response: {modified_response}")
        return modified_response

    print("[Callback] Passing original tool response through.")
    return None

my_llm_agent = LlmAgent(
    name="AfterToolCallbackAgent",
    model=GEMINI_2_FLASH,
    instruction="You are an agent that finds capital cities using the get_capital_city tool. Report the result clearly.",
    description="An LLM agent demonstrating after_tool_callback",
    tools=[capital_tool],
    after_tool_callback=simple_after_tool_modifier
)

APP_NAME = "guardrail_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=my_llm_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner

async def call_agent_async(query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            print("Agent Response: ", event.content.parts[0].text)

await call_agent_async("united states")
```
