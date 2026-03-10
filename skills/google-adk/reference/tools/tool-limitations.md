# Limitations for ADK tools

Some ADK tools have limitations that can impact how you implement them within an
agent workflow. This page lists these tool limitations and workarounds, if available.

## One tool per agent limitation

ONLY for Search in ADK Python v1.15.0 and lower

This limitation only applies to the use of Google Search and Vertex AI Search
tools in ADK Python v1.15.0 and lower. ADK Python release v1.16.0 and higher
provides a built-in workaround to remove this limitation.

In general, you can use more than one tool in an agent, but use of specific
tools within an agent excludes the use of any other tools in that agent. The
following ADK Tools can only be used by themselves, without any other tools, in
a single agent object:

* Code Execution with Gemini API
* Google Search with Gemini API
* Vertex AI Search

For example, the following approach that uses one of these tools along with
other tools, within a single agent, is ***not supported***:


```
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.5-flash",
    description="Code Agent",
    tools=[custom_function],
    code_executor=BuiltInCodeExecutor() # <-- NOT supported when used with tools
)
```

### Workaround #1: AgentTool.create() method

PythonJava

The following code sample demonstrates how to use multiple built-in tools or how
to use built-in tools with other tools by using multiple agents:


```
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.code_executors import BuiltInCodeExecutor

search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="""
    You're a specialist in Google Search
    """,
    tools=[google_search],
)
coding_agent = Agent(
    model='gemini-2.0-flash',
    name='CodeAgent',
    instruction="""
    You're a specialist in Code Execution
    """,
    code_executor=BuiltInCodeExecutor(),
)
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    description="Root Agent",
    tools=[AgentTool(agent=search_agent), AgentTool(agent=coding_agent)],
)
```

### Workaround #2: bypass\_multi\_tools\_limit

PythonJava

ADK Python has a built-in workaround which bypasses this limitation for
`GoogleSearchTool` and `VertexAiSearchTool` (use `bypass_multi_tools_limit=True` to enable it),
as shown in the
[built\_in\_multi\_tools](https://github.com/google/adk-python/tree/main/contributing/samples/built_in_multi_tools).
sample agent.


Built-in tools cannot be used within a sub-agent, with the exception of
`GoogleSearchTool` and `VertexAiSearchTool` in ADK Python because of the
workaround mentioned above.

For example, the following approach that uses built-in tools within sub-agents
is **not supported**:


```
url_context_agent = Agent(
    model='gemini-2.5-flash',
    name='UrlContextAgent',
    instruction="""
    You're a specialist in URL Context
    """,
    tools=[url_context],
)
coding_agent = Agent(
    model='gemini-2.5-flash',
    name='CodeAgent',
    instruction="""
    You're a specialist in Code Execution
    """,
    code_executor=BuiltInCodeExecutor(),
)
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.5-flash",
    description="Root Agent",
    sub_agents=[
        url_context_agent,
        coding_agent
    ],
)
```