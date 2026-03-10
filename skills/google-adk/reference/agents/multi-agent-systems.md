# Multi-Agent Systems in ADK

As agentic applications grow in complexity, structuring them as a single, monolithic agent can become challenging to develop, maintain, and reason about. The Agent Development Kit (ADK) supports building sophisticated applications by composing multiple, distinct `BaseAgent` instances into a **Multi-Agent System (MAS)**.

In ADK, a multi-agent system is an application where different agents, often forming a hierarchy, collaborate or coordinate to achieve a larger goal. Structuring your application this way offers significant advantages, including enhanced modularity, specialization, reusability, maintainability, and the ability to define structured control flows using dedicated workflow agents.

You can compose various types of agents derived from `BaseAgent` to build these systems:

* **LLM Agents:** Agents powered by large language models. (See [LLM Agents](llm-agents.md))
* **Workflow Agents:** Specialized agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`) designed to manage the execution flow of their sub-agents. (See [Workflow Agents](workflow-agents.md))
* **Custom agents:** Your own agents inheriting from `BaseAgent` with specialized, non-LLM logic. (See [Custom Agents](custom-agents.md))

The following sections detail the core ADK primitives—such as agent hierarchy, workflow agents, and interaction mechanisms—that enable you to construct and manage these multi-agent systems effectively.

## 1. ADK Primitives for Agent Composition

ADK provides core building blocks—primitives—that enable you to structure and manage interactions within your multi-agent system.

> **Note:** The specific parameters or method names for the primitives may vary slightly by SDK language (e.g., `sub_agents` in Python, `subAgents` in Java). Refer to the language-specific API documentation for details.

### 1.1. Agent Hierarchy (Parent agent, Sub Agents)

The foundation for structuring multi-agent systems is the parent-child relationship defined in `BaseAgent`.

* **Establishing Hierarchy:** You create a tree structure by passing a list of agent instances to the `sub_agents` argument when initializing a parent agent. ADK automatically sets the `parent_agent` attribute on each child agent during initialization.
* **Single Parent Rule:** An agent instance can only be added as a sub-agent once. Attempting to assign a second parent will result in a `ValueError`.
* **Importance:** This hierarchy defines the scope for workflow agents and influences the potential targets for LLM-Driven Delegation. You can navigate the hierarchy using `agent.parent_agent` or find descendants using `agent.find_agent(name)`.

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

### 1.2. Workflow Agents as Orchestrators

ADK includes specialized agents derived from `BaseAgent` that don't perform tasks themselves but orchestrate the execution flow of their `sub_agents`.

* **[`SequentialAgent`](workflow/sequential-agents.md):** Executes its `sub_agents` one after another in the order they are listed.
  + **Context:** Passes the *same* `InvocationContext` sequentially, allowing agents to easily pass results via shared state.

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

* **[`ParallelAgent`](workflow/parallel-agents.md):** Executes its `sub_agents` in parallel. Events from sub-agents may be interleaved.
  + **Context:** Modifies the `InvocationContext.branch` for each child agent (e.g., `ParentBranch.ChildName`), providing a distinct contextual path which can be useful for isolating history in some memory implementations.
  + **State:** Despite different branches, all parallel children access the *same shared* `session.state`, enabling them to read initial state and write results (use distinct keys to avoid race conditions).

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

* **[`LoopAgent`](workflow/loop-agents.md):** Executes its `sub_agents` sequentially in a loop.
  + **Termination:** The loop stops if the optional `max_iterations` is reached, or if any sub-agent returns an `Event` with `escalate=True` in its Event Actions.
  + **Context & State:** Passes the *same* `InvocationContext` in each iteration, allowing state changes (e.g., counters, flags) to persist across loops.

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

### 1.3. Interaction & Communication Mechanisms

Agents within a system often need to exchange data or trigger actions in one another. ADK facilitates this through:

#### a) Shared Session State (`session.state`)

The most fundamental way for agents operating within the same invocation (and thus sharing the same `Session` object via the `InvocationContext`) to communicate passively.

* **Mechanism:** One agent (or its tool/callback) writes a value (`context.state['data_key'] = processed_data`), and a subsequent agent reads it (`data = context.state.get('data_key')`). State changes are tracked via [Callbacks](../callbacks/callbacks-overview.md).
* **Convenience:** The `output_key` property on [`LlmAgent`](llm-agents.md) automatically saves the agent's final response text (or structured output) to the specified state key.
* **Nature:** Asynchronous, passive communication. Ideal for pipelines orchestrated by `SequentialAgent` or passing data across `LoopAgent` iterations.
* **See Also:** [Sessions](../sessions/sessions-overview.md)

> **Invocation Context and `temp:` State:** When a parent agent invokes a sub-agent, it passes the same `InvocationContext`. This means they share the same temporary (`temp:`) state, which is ideal for passing data that is only relevant for the current turn.

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

#### b) LLM-Driven Delegation (Agent Transfer)

Leverages an [`LlmAgent`](llm-agents.md)'s understanding to dynamically route tasks to other suitable agents within the hierarchy.

* **Mechanism:** The agent's LLM generates a specific function call: `transfer_to_agent(agent_name='target_agent_name')`.
* **Handling:** The `AutoFlow`, used by default when sub-agents are present or transfer isn't disallowed, intercepts this call. It identifies the target agent using `root_agent.find_agent()` and updates the `InvocationContext` to switch execution focus.
* **Requires:** The calling `LlmAgent` needs clear `instructions` on when to transfer, and potential target agents need distinct `description`s for the LLM to make informed decisions. Transfer scope (parent, sub-agent, siblings) can be configured on the `LlmAgent`.
* **Nature:** Dynamic, flexible routing based on LLM interpretation.

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

#### c) Explicit Invocation (`AgentTool`)

Allows an [`LlmAgent`](llm-agents.md) to treat another `BaseAgent` instance as a callable function or [Tool](../tools/).

* **Mechanism:** Wrap the target agent instance in `AgentTool` and include it in the parent `LlmAgent`'s `tools` list. `AgentTool` generates a corresponding function declaration for the LLM.
* **Handling:** When the parent LLM generates a function call targeting the `AgentTool`, the framework executes `AgentTool.run_async`. This method runs the target agent, captures its final response, forwards any state/artifact changes back to the parent's context, and returns the response as the tool's result.
* **Nature:** Synchronous (within the parent's flow), explicit, controlled invocation like any other tool.
* **(Note:** `AgentTool` needs to be imported and used explicitly).

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

These primitives provide the flexibility to design multi-agent interactions ranging from tightly coupled sequential workflows to dynamic, LLM-driven delegation networks.

## 2. Common Multi-Agent Patterns using ADK Primitives

By combining ADK's composition primitives, you can implement various established patterns for multi-agent collaboration.

### Coordinator/Dispatcher Pattern

* **Structure:** A central [`LlmAgent`](llm-agents.md) (Coordinator) manages several specialized `sub_agents`.
* **Goal:** Route incoming requests to the appropriate specialist agent.
* **ADK Primitives Used:**
  + **Hierarchy:** Coordinator has specialists listed in `sub_agents`.
  + **Interaction:** Primarily uses **LLM-Driven Delegation** (requires clear `description`s on sub-agents and appropriate `instruction` on Coordinator) or **Explicit Invocation (`AgentTool`)** (Coordinator includes `AgentTool`-wrapped specialists in its `tools`).

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

### Sequential Pipeline Pattern

* **Structure:** A [`SequentialAgent`](workflow/sequential-agents.md) contains `sub_agents` executed in a fixed order.
* **Goal:** Implement a multistep process where the output of one step feeds into the next.
* **ADK Primitives Used:**
  + **Workflow:** `SequentialAgent` defines the order.
  + **Communication:** Primarily uses **Shared Session State**. Earlier agents write results (often via `output_key`), later agents read those results from `context.state`.

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

### Parallel Fan-Out/Gather Pattern

* **Structure:** A [`ParallelAgent`](workflow/parallel-agents.md) runs multiple `sub_agents` concurrently, often followed by a later agent (in a `SequentialAgent`) that aggregates results.
* **Goal:** Execute independent tasks simultaneously to reduce latency, then combine their outputs.
* **ADK Primitives Used:**
  + **Workflow:** `ParallelAgent` for concurrent execution (Fan-Out). Often nested within a `SequentialAgent` to handle the subsequent aggregation step (Gather).
  + **Communication:** Sub-agents write results to distinct keys in **Shared Session State**. The subsequent "Gather" agent reads multiple state keys.

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

### Hierarchical Task Decomposition

* **Structure:** A multi-level tree of agents where higher-level agents break down complex goals and delegate sub-tasks to lower-level agents.
* **Goal:** Solve complex problems by recursively breaking them down into simpler, executable steps.
* **ADK Primitives Used:**
  + **Hierarchy:** Multi-level `parent_agent`/`sub_agents` structure.
  + **Interaction:** Primarily **LLM-Driven Delegation** or **Explicit Invocation (`AgentTool`)** used by parent agents to assign tasks to subagents. Results are returned up the hierarchy (via tool responses or state).

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

### Review/Critique Pattern (Generator-Critic)

* **Structure:** Typically involves two agents within a [`SequentialAgent`](workflow/sequential-agents.md): a Generator and a Critic/Reviewer.
* **Goal:** Improve the quality or validity of generated output by having a dedicated agent review it.
* **ADK Primitives Used:**
  + **Workflow:** `SequentialAgent` ensures generation happens before review.
  + **Communication:** **Shared Session State** (Generator uses `output_key` to save output; Reviewer reads that state key). The Reviewer might save its feedback to another state key for subsequent steps.

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

### Iterative Refinement Pattern

* **Structure:** Uses a [`LoopAgent`](workflow/loop-agents.md) containing one or more agents that work on a task over multiple iterations.
* **Goal:** Progressively improve a result (e.g., code, text, plan) stored in the session state until a quality threshold is met or a maximum number of iterations is reached.
* **ADK Primitives Used:**
  + **Workflow:** `LoopAgent` manages the repetition.
  + **Communication:** **Shared Session State** is essential for agents to read the previous iteration's output and save the refined version.
  + **Termination:** The loop typically ends based on `max_iterations` or a dedicated checking agent setting `escalate=True` in the `Event Actions` when the result is satisfactory.

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

### Human-in-the-Loop Pattern

* **Structure:** Integrates human intervention points within an agent workflow.
* **Goal:** Allow for human oversight, approval, correction, or tasks that AI cannot perform.
* **ADK Primitives Used (Conceptual):**
  + **Interaction:** Can be implemented using a custom **Tool** that pauses execution and sends a request to an external system (e.g., a UI, ticketing system) waiting for human input. The tool then returns the human's response to the agent.
  + **Workflow:** Could use **LLM-Driven Delegation** (`transfer_to_agent`) targeting a conceptual "Human Agent" that triggers the external workflow, or use the custom tool within an `LlmAgent`.
  + **State/Callbacks:** State can hold task details for the human; callbacks can manage the interaction flow.
  + **Note:** ADK doesn't have a built-in "Human Agent" type, so this requires custom integration.

> *Code examples: see [multi-agent-systems-python.md](multi-agent-systems-python.md), [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md), [multi-agent-systems-go.md](multi-agent-systems-go.md), [multi-agent-systems-java.md](multi-agent-systems-java.md)*

#### Human in the Loop with Policy

A more advanced and structured way to implement Human-in-the-Loop is by using a `PolicyEngine`. This approach allows you to define policies that can trigger a confirmation step from a user before a tool is executed. The `SecurityPlugin` intercepts a tool call, consults the `PolicyEngine`, and if the policy dictates, it will automatically request user confirmation. This pattern is more robust for enforcing governance and security rules.

Here's how it works:

1. **`SecurityPlugin`**: You add this plugin to your `Runner`. It acts as an interceptor for all tool calls.
2. **`BasePolicyEngine`**: You create a custom class that implements this interface. Its `evaluate()` method contains your logic to decide if a tool call needs confirmation.
3. **`PolicyOutcome.CONFIRM`**: When your `evaluate()` method returns this outcome, the `SecurityPlugin` pauses the tool execution and generates a special `FunctionCall` using `getAskUserConfirmationFunctionCalls`.
4. **Application Handling**: Your application code receives this special function call and presents the confirmation request to the user.
5. **User Confirmation**: Once the user confirms, your application sends a `FunctionResponse` back to the agent, which allows the `SecurityPlugin` to proceed with the original tool execution.

> **TypeScript Recommended Pattern:** The Policy-based pattern is the recommended approach for implementing Human-in-the-Loop workflows in TypeScript. Support in other ADK languages is planned for future releases.

A conceptual example of using a `CustomPolicyEngine` to require user confirmation before executing any tool is shown below.

> *Code examples: see [multi-agent-systems-typescript.md](multi-agent-systems-typescript.md)*

### Combining Patterns

These patterns provide starting points for structuring your multi-agent systems. You can mix and match them as needed to create the most effective architecture for your specific application.
