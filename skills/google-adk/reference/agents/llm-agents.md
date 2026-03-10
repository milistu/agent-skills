# LLM Agent

The `LlmAgent` (often aliased simply as `Agent`) is a core component in ADK, acting as the "thinking" part of your application. It leverages the power of a Large Language Model (LLM) for reasoning, understanding natural language, making decisions, generating responses, and interacting with tools.

Unlike deterministic [Workflow Agents](../agents/workflow-agents.md) that follow predefined execution paths, `LlmAgent` behavior is non-deterministic. It uses the LLM to interpret instructions and context, deciding dynamically how to proceed, which tools to use (if any), or whether to transfer control to another agent.

Building an effective `LlmAgent` involves defining its identity, clearly guiding its behavior through instructions, and equipping it with the necessary tools and capabilities.

## Defining the Agent's Identity and Purpose

First, you need to establish what the agent *is* and what it's *for*.

* **`name` (Required):** Every agent needs a unique string identifier. This `name` is crucial for internal operations, especially in multi-agent systems where agents need to refer to or delegate tasks to each other. Choose a descriptive name that reflects the agent's function (e.g., `customer_support_router`, `billing_inquiry_agent`). Avoid reserved names like `user`.
* **`description` (Optional, Recommended for Multi-Agent):** Provide a concise summary of the agent's capabilities. This description is primarily used by *other* LLM agents to determine if they should route a task to this agent. Make it specific enough to differentiate it from peers (e.g., "Handles inquiries about current billing statements," not just "Billing agent").
* **`model` (Required):** Specify the underlying LLM that will power this agent's reasoning. This is a string identifier like `"gemini-2.5-flash"`. The choice of model impacts the agent's capabilities, cost, and performance. See the Models page for available options and considerations.

## Guiding the Agent: Instructions (`instruction`)

The `instruction` parameter is arguably the most critical for shaping an `LlmAgent`'s behavior. It's a string (or a function returning a string) that tells the agent:

* Its core task or goal.
* Its personality or persona (e.g., "You are a helpful assistant," "You are a witty pirate").
* Constraints on its behavior (e.g., "Only answer questions about X," "Never reveal Y").
* How and when to use its `tools`. You should explain the purpose of each tool and the circumstances under which it should be called, supplementing any descriptions within the tool itself.
* The desired format for its output (e.g., "Respond in JSON," "Provide a bulleted list").

**Tips for Effective Instructions:**

* **Be Clear and Specific:** Avoid ambiguity. Clearly state the desired actions and outcomes.
* **Use Markdown:** Improve readability for complex instructions using headings, lists, etc.
* **Provide Examples (Few-Shot):** For complex tasks or specific output formats, include examples directly in the instruction.
* **Guide Tool Use:** Don't just list tools; explain *when* and *why* the agent should use them.

**State:**

* The instruction is a string template; you can use the `{var}` syntax to insert dynamic values into the instruction.
* `{var}` is used to insert the value of the state variable named `var`.
* `{artifact.var}` is used to insert the text content of the artifact named `var`.
* If the state variable or artifact does not exist, the agent will raise an error. If you want to ignore the error, you can append a `?` to the variable name as in `{var?}`.

> *Code examples: see [llm-agents-python.md](llm-agents-python.md), [llm-agents-typescript.md](llm-agents-typescript.md), [llm-agents-go.md](llm-agents-go.md), [llm-agents-java.md](llm-agents-java.md)*

*(Note: For instructions that apply to* all *agents in a system, consider using `global_instruction` on the root agent, detailed further in the Multi-Agents section.)*

## Equipping the Agent: Tools (`tools`)

Tools give your `LlmAgent` capabilities beyond the LLM's built-in knowledge or reasoning. They allow the agent to interact with the outside world, perform calculations, fetch real-time data, or execute specific actions.

* **`tools` (Optional):** Provide a list of tools the agent can use. Each item in the list can be:
  + A native function or method (wrapped as a `FunctionTool`). Python ADK automatically wraps the native function into a `FunctionTool` whereas, you must explicitly wrap your Java methods using `FunctionTool.create(...)`
  + An instance of a class inheriting from `BaseTool`.
  + An instance of another agent (`AgentTool`, enabling agent-to-agent delegation — see Multi-Agents).

The LLM uses the function/tool names, descriptions (from docstrings or the `description` field), and parameter schemas to decide which tool to call based on the conversation and its instructions.

> *Code examples: see [llm-agents-python.md](llm-agents-python.md), [llm-agents-typescript.md](llm-agents-typescript.md), [llm-agents-go.md](llm-agents-go.md), [llm-agents-java.md](llm-agents-java.md)*

Learn more about Tools in Custom Tools.

## Advanced Configuration & Control

Beyond the core parameters, `LlmAgent` offers several options for finer control:

### Fine-Tuning LLM Generation (`generate_content_config`)

You can adjust how the underlying LLM generates responses using `generate_content_config`.

* **`generate_content_config` (Optional):** Pass an instance of `google.genai.types.GenerateContentConfig` to control parameters like `temperature` (randomness), `max_output_tokens` (response length), `top_p`, `top_k`, and safety settings.

> *Code examples: see [llm-agents-python.md](llm-agents-python.md), [llm-agents-typescript.md](llm-agents-typescript.md), [llm-agents-go.md](llm-agents-go.md), [llm-agents-java.md](llm-agents-java.md)*

### Structuring Data (`input_schema`, `output_schema`, `output_key`)

For scenarios requiring structured data exchange with an `LLM Agent`, the ADK provides mechanisms to define expected input and desired output formats using schema definitions.

* **`input_schema` (Optional):** Define a schema representing the expected input structure. If set, the user message content passed to this agent *must* be a JSON string conforming to this schema. Your instructions should guide the user or preceding agent accordingly.
* **`output_schema` (Optional):** Define a schema representing the desired output structure. If set, the agent's final response *must* be a JSON string conforming to this schema.

> **Warning: Using `output_schema` with `tools`**
>
> Using `output_schema` with `tools` in the same LLM request is only supported by specific models, including Gemini 3.0. For other models, workarounds using function tools in ADK may not work reliably. In such cases, consider using sub-agents that handle output formatting separately.

* **`output_key` (Optional):** Provide a string key. If set, the text content of the agent's *final* response will be automatically saved to the session's state dictionary under this key. This is useful for passing results between agents or steps in a workflow.
  + In Python, this might look like: `session.state[output_key] = agent_response_text`
  + In Java: `session.state().put(outputKey, agentResponseText)`
  + In Golang, within a callback handler: `ctx.State().Set(output_key, agentResponseText)`

In Python, the input and output schema is typically a `Pydantic` `BaseModel`. In Go and Java, it is a `google.genai.types.Schema` object.

> *Code examples: see [llm-agents-python.md](llm-agents-python.md), [llm-agents-typescript.md](llm-agents-typescript.md), [llm-agents-go.md](llm-agents-go.md), [llm-agents-java.md](llm-agents-java.md)*

### Managing Context (`include_contents`)

Control whether the agent receives the prior conversation history.

* **`include_contents` (Optional, Default: `'default'`):** Determines if the `contents` (history) are sent to the LLM.
  + `'default'`: The agent receives the relevant conversation history.
  + `'none'`: The agent receives no prior `contents`. It operates based solely on its current instruction and any input provided in the *current* turn (useful for stateless tasks or enforcing specific contexts).

### Planner

**`planner` (Optional):** Assign a `BasePlanner` instance to enable multi-step reasoning and planning before execution. There are two main planners:

* **`BuiltInPlanner`:** Leverages the model's built-in planning capabilities (e.g., Gemini's thinking feature). The `thinking_budget` parameter guides the model on the number of thinking tokens to use when generating a response. The `include_thoughts` parameter controls whether the model should include its raw thoughts and internal reasoning process in the response.

* **`PlanReActPlanner`:** This planner instructs the model to follow a specific structure in its output: first create a plan, then execute actions (like calling tools), and provide reasoning for its steps. *It's particularly useful for models that don't have a built-in "thinking" feature*.

  The agent's response will follow a structured format with `/*PLANNING*/`, `/*ACTION*/`, `/*REASONING*/`, and `/*FINAL_ANSWER*/` markers.

> *Code examples: see [llm-agents-python.md](llm-agents-python.md)*

### Code Execution

* **`code_executor` (Optional):** Provide a `BaseCodeExecutor` instance to allow the agent to execute code blocks found in the LLM's response. For more information, see Code Execution with Gemini API.

> *Code examples: see [llm-agents-python.md](llm-agents-python.md), [llm-agents-java.md](llm-agents-java.md)*

## Putting It Together: Example

Here's the complete `capital_agent` example demonstrating `LlmAgent` with tools vs. output schema side by side. It shows how to wire `input_schema`, `output_schema`, `output_key`, tools, sessions, and runners together end to end.

> *Code examples: see [llm-agents-python.md](llm-agents-python.md), [llm-agents-typescript.md](llm-agents-typescript.md), [llm-agents-go.md](llm-agents-go.md), [llm-agents-java.md](llm-agents-java.md)*

*(This example demonstrates the core concepts. More complex agents might incorporate schemas, context control, planning, etc.)*

## Related Concepts

While this page covers the core configuration of `LlmAgent`, several related concepts provide more advanced control and are detailed elsewhere:

* **Callbacks:** Intercepting execution points (before/after model calls, before/after tool calls) using `before_model_callback`, `after_model_callback`, etc. See Callbacks.
* **Multi-Agent Control:** Advanced strategies for agent interaction, including planning (`planner`), controlling agent transfer (`disallow_transfer_to_parent`, `disallow_transfer_to_peers`), and system-wide instructions (`global_instruction`). See Multi-Agents.
