# LLM Agent — Python Examples

## Instructions with State Templating

Demonstrates `{var}` template syntax in instructions and how to wire a tool alongside the instruction.

```python
capital_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="capital_agent",
    description="Answers user questions about the capital city of a given country.",
    instruction="""You are an agent that provides the capital city of a country.
When a user asks for the capital of a country:
1. Identify the country name from the user's query.
2. Use the `get_capital_city` tool to find the capital.
3. Respond clearly to the user, stating the capital city.
Example Query: "What's the capital of {country}?"
Example Response: "The capital of France is Paris."
""",
    # tools will be added next
)
```

## Equipping the Agent: Tools

Demonstrates defining a plain Python function as a tool and passing it directly to `LlmAgent`; ADK auto-wraps it as a `FunctionTool`.

```python
def get_capital_city(country: str) -> str:
    """Retrieves the capital city for a given country."""
    # Replace with actual logic (e.g., API call, database lookup)
    capitals = {"france": "Paris", "japan": "Tokyo", "canada": "Ottawa"}
    return capitals.get(country.lower(), f"Sorry, I don't know the capital of {country}.")

capital_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="capital_agent",
    description="Answers user questions about the capital city of a given country.",
    instruction="You are an agent that provides the capital city of a country...",
    tools=[get_capital_city],  # Provide the function directly
)
```

## Fine-Tuning LLM Generation (`generate_content_config`)

Demonstrates configuring `temperature`, `max_output_tokens`, and safety settings via `GenerateContentConfig`.

```python
from google.genai import types

agent = LlmAgent(
    # ... other params
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,  # More deterministic output
        max_output_tokens=250,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            )
        ]
    )
)
```

## Structured Output (`output_schema` + `output_key`)

Demonstrates using a Pydantic `BaseModel` as `output_schema` to enforce JSON output, and `output_key` to store the result in session state. Note: tools cannot be used effectively alongside `output_schema`.

```python
from pydantic import BaseModel, Field

class CapitalOutput(BaseModel):
    capital: str = Field(description="The capital of the country.")

structured_capital_agent = LlmAgent(
    # ... name, model, description
    instruction="""You are a Capital Information Agent. Given a country, respond ONLY with a JSON object containing the capital. Format: {"capital": "capital_name"}""",
    output_schema=CapitalOutput,       # Enforce JSON output
    output_key="found_capital"         # Store result in state['found_capital']
    # Cannot use tools=[get_capital_city] effectively here
)
```

## Planner: BuiltInPlanner

Demonstrates using `BuiltInPlanner` with `ThinkingConfig` to enable the model's native thinking feature with a token budget.

```python
from google.adk import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types

my_agent = Agent(
    model="gemini-2.5-flash",
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),
    # ... your tools here
)
```

## Planner: PlanReActPlanner

Demonstrates using `PlanReActPlanner` for models without a built-in thinking feature; the agent outputs structured `/*PLANNING*/` / `/*FINAL_ANSWER*/` sections.

```python
from google.adk import Agent
from google.adk.planners import PlanReActPlanner

my_agent = Agent(
    model="gemini-2.5-flash",
    planner=PlanReActPlanner(),
    # ... your tools here
)
```

## Planner: Full BuiltInPlanner End-to-End

Full runnable example wiring `BuiltInPlanner` with `ThinkingConfig`, two tools, a `Runner`, and a session service together.

```python
import asyncio
import datetime
from zoneinfo import ZoneInfo

from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.planners import BuiltInPlanner
from google.genai.types import ThinkingConfig

APP_NAME = "weather_app"
USER_ID = "1234"
SESSION_ID = "session1234"

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city."""
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have timezone information for {city}.",
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    return {"status": "success", "report": report}


# Step 1: Create a ThinkingConfig
thinking_config = ThinkingConfig(
    include_thoughts=True,  # Ask the model to include its thoughts in the response
    thinking_budget=256     # Limit the 'thinking' to 256 tokens (adjust as needed)
)

# Step 2: Instantiate BuiltInPlanner
planner = BuiltInPlanner(thinking_config=thinking_config)

# Step 3: Wrap the planner in an LlmAgent
agent = LlmAgent(
    model="gemini-2.5-pro-preview-03-25",
    name="weather_and_time_agent",
    instruction="You are an agent that returns time and weather",
    planner=planner,
    tools=[get_weather, get_current_time]
)

# Session and Runner
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

# Agent Interaction
def call_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        if event.is_final_response() and event.content:
            final_answer = event.content.parts[0].text.strip()
            print("FINAL ANSWER:", final_answer)

call_agent("If it's raining in New York right now, what is the current temperature?")
```

## Code Execution

Full runnable example using `BuiltInCodeExecutor` to let the agent write and execute Python code, with event-loop handling for both script and Jupyter/Colab environments.

```python
import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai import types

AGENT_NAME = "calculator_agent"
APP_NAME = "calculator"
USER_ID = "user1234"
SESSION_ID = "session_code_exec_async"
GEMINI_MODEL = "gemini-2.0-flash"

# Agent Definition
code_agent = LlmAgent(
    name=AGENT_NAME,
    model=GEMINI_MODEL,
    code_executor=BuiltInCodeExecutor(),
    instruction="""You are a calculator agent.
    When given a mathematical expression, write and execute Python code to calculate the result.
    Return only the final numerical result as plain text, without markdown or code blocks.
    """,
    description="Executes Python code to perform calculations.",
)

# Session and Runner
session_service = InMemorySessionService()
session = asyncio.run(session_service.create_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
))
runner = Runner(agent=code_agent, app_name=APP_NAME, session_service=session_service)

# Agent Interaction (Async) — inspects executable_code and code_execution_result parts
async def call_agent_async(query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(f"\n--- Running Query: {query} ---")
    final_response_text = "No final text response captured."
    try:
        async for event in runner.run_async(
            user_id=USER_ID, session_id=SESSION_ID, new_message=content
        ):
            print(f"Event ID: {event.id}, Author: {event.author}")

            has_specific_part = False
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.executable_code:
                        print(f"  Debug: Agent generated code:\n```python\n{part.executable_code.code}\n```")
                        has_specific_part = True
                    elif part.code_execution_result:
                        print(
                            f"  Debug: Code Execution Result: {part.code_execution_result.outcome}"
                            f" - Output:\n{part.code_execution_result.output}"
                        )
                        has_specific_part = True
                    elif part.text and not part.text.isspace():
                        print(f"  Text: '{part.text.strip()}'")

            if not has_specific_part and event.is_final_response():
                if event.content and event.content.parts and event.content.parts[0].text:
                    final_response_text = event.content.parts[0].text.strip()
                    print(f"==> Final Agent Response: {final_response_text}")
                else:
                    print("==> Final Agent Response: [No text content in final event]")

    except Exception as e:
        print(f"ERROR during agent run: {e}")
    print("-" * 30)


async def main():
    await call_agent_async("Calculate the value of (5 + 7) * 3")
    await call_agent_async("What is 10 factorial?")


try:
    asyncio.run(main())
except RuntimeError as e:
    if "cannot be called from a running event loop" in str(e):
        print("\nRunning in an existing event loop (like Colab/Jupyter).")
        print("Please run `await main()` in a notebook cell instead.")
    else:
        raise e
```

## Putting It Together: Full End-to-End Example

Full runnable example contrasting two agents side by side: one uses a tool + `output_key`, the other uses `output_schema` + `output_key` (no tools). Shows `input_schema` (Pydantic), `Runner`, `InMemorySessionService`, async event iteration, and reading back session state.

```python
import json
import asyncio

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel, Field

APP_NAME = "agent_comparison_app"
USER_ID = "test_user_456"
SESSION_ID_TOOL_AGENT = "session_tool_agent_xyz"
SESSION_ID_SCHEMA_AGENT = "session_schema_agent_xyz"
MODEL_NAME = "gemini-2.0-flash"

# --- Schemas ---

class CountryInput(BaseModel):
    country: str = Field(description="The country to get information about.")

class CapitalInfoOutput(BaseModel):
    capital: str = Field(description="The capital city of the country.")
    population_estimate: str = Field(description="An estimated population of the capital city.")

# --- Tool ---

def get_capital_city(country: str) -> str:
    """Retrieves the capital city of a given country."""
    print(f"\n-- Tool Call: get_capital_city(country='{country}') --")
    country_capitals = {
        "united states": "Washington, D.C.",
        "canada": "Ottawa",
        "france": "Paris",
        "japan": "Tokyo",
    }
    result = country_capitals.get(country.lower(), f"Sorry, I couldn't find the capital for {country}.")
    print(f"-- Tool Result: '{result}' --")
    return result

# --- Agent 1: Uses a tool and output_key ---
capital_agent_with_tool = LlmAgent(
    model=MODEL_NAME,
    name="capital_agent_tool",
    description="Retrieves the capital city using a specific tool.",
    instruction="""You are a helpful agent that provides the capital city of a country using a tool.
The user will provide the country name in a JSON format like {"country": "country_name"}.
1. Extract the country name.
2. Use the `get_capital_city` tool to find the capital.
3. Respond clearly to the user, stating the capital city found by the tool.
""",
    tools=[get_capital_city],
    input_schema=CountryInput,
    output_key="capital_tool_result",
)

# --- Agent 2: Uses output_schema (NO tools possible) ---
structured_info_agent_schema = LlmAgent(
    model=MODEL_NAME,
    name="structured_info_agent_schema",
    description="Provides capital and estimated population in a specific JSON format.",
    instruction=f"""You are an agent that provides country information.
The user will provide the country name in a JSON format like {{"country": "country_name"}}.
Respond ONLY with a JSON object matching this exact schema:
{json.dumps(CapitalInfoOutput.model_json_schema(), indent=2)}
Use your knowledge to determine the capital and estimate the population. Do not use any tools.
""",
    input_schema=CountryInput,
    output_schema=CapitalInfoOutput,
    output_key="structured_info_result",
)

# --- Session service and runners ---
session_service = InMemorySessionService()

capital_runner = Runner(
    agent=capital_agent_with_tool,
    app_name=APP_NAME,
    session_service=session_service,
)
structured_runner = Runner(
    agent=structured_info_agent_schema,
    app_name=APP_NAME,
    session_service=session_service,
)

# --- Interaction helper ---
async def call_agent_and_print(runner_instance, agent_instance, session_id, query_json):
    """Sends a query to the agent/runner and prints the response + stored session state."""
    print(f"\n>>> Calling Agent: '{agent_instance.name}' | Query: {query_json}")
    user_content = types.Content(role='user', parts=[types.Part(text=query_json)])

    final_response_content = "No final response received."
    async for event in runner_instance.run_async(
        user_id=USER_ID, session_id=session_id, new_message=user_content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response_content = event.content.parts[0].text

    print(f"<<< Agent '{agent_instance.name}' Response: {final_response_content}")

    current_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    stored_output = current_session.state.get(agent_instance.output_key)

    print(f"--- Session State ['{agent_instance.output_key}']: ", end="")
    try:
        parsed_output = json.loads(stored_output)
        print(json.dumps(parsed_output, indent=2))
    except (json.JSONDecodeError, TypeError):
        print(stored_output)
    print("-" * 30)


async def main():
    print("--- Creating Sessions ---")
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_TOOL_AGENT)
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_SCHEMA_AGENT)

    print("--- Testing Agent with Tool ---")
    await call_agent_and_print(capital_runner, capital_agent_with_tool, SESSION_ID_TOOL_AGENT, '{"country": "France"}')
    await call_agent_and_print(capital_runner, capital_agent_with_tool, SESSION_ID_TOOL_AGENT, '{"country": "Canada"}')

    print("\n--- Testing Agent with Output Schema (No Tool Use) ---")
    await call_agent_and_print(structured_runner, structured_info_agent_schema, SESSION_ID_SCHEMA_AGENT, '{"country": "France"}')
    await call_agent_and_print(structured_runner, structured_info_agent_schema, SESSION_ID_SCHEMA_AGENT, '{"country": "Japan"}')


if __name__ == "__main__":
    asyncio.run(main())
```
