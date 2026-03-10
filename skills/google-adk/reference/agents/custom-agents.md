# Custom Agents

Custom agents provide the ultimate flexibility in ADK, allowing you to define **arbitrary orchestration logic** by inheriting directly from `BaseAgent` and implementing your own control flow. This goes beyond the predefined patterns of `SequentialAgent`, `LoopAgent`, and `ParallelAgent`, enabling you to build highly specific and complex agentic workflows.

> **Advanced Concept:** Building custom agents by directly implementing `_run_async_impl` (or its equivalent in other languages) provides powerful control but is more complex than using the predefined `LlmAgent` or standard workflow agent types. Understanding those foundational agent types first is recommended before tackling custom orchestration logic.

## Introduction: Beyond Predefined Workflows

### What is a Custom Agent?

A Custom Agent is essentially any class you create that inherits from `google.adk.agents.BaseAgent` and implements its core execution logic within the `_run_async_impl` asynchronous method. You have complete control over how this method calls other agents (sub-agents), manages state, and handles events.

> **Note:** The specific method name for implementing an agent's core asynchronous logic may vary slightly by SDK language (e.g., `runAsyncImpl` in Java, `_run_async_impl` in Python, or `runAsyncImpl` in TypeScript). Refer to the language-specific API documentation for details.

### Why Use Them?

While the standard [Workflow Agents](workflow-agents.md) (`SequentialAgent`, `LoopAgent`, `ParallelAgent`) cover common orchestration patterns, you'll need a Custom agent when your requirements include:

* **Conditional Logic:** Executing different sub-agents or taking different paths based on runtime conditions or the results of previous steps.
* **Complex State Management:** Implementing intricate logic for maintaining and updating state throughout the workflow beyond simple sequential passing.
* **External Integrations:** Incorporating calls to external APIs, databases, or custom libraries directly within the orchestration flow control.
* **Dynamic Agent Selection:** Choosing which sub-agent(s) to run next based on dynamic evaluation of the situation or input.
* **Unique Workflow Patterns:** Implementing orchestration logic that doesn't fit the standard sequential, parallel, or loop structures.

## Implementing Custom Logic

The core of any custom agent is the method where you define its unique asynchronous behavior. This method allows you to orchestrate sub-agents and manage the flow of execution.

**Python** — The heart of any custom agent is the `_run_async_impl` method.

* **Signature:** `async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:`
* **Asynchronous Generator:** It must be an `async def` function and return an `AsyncGenerator`. This allows it to `yield` events produced by sub-agents or its own logic back to the runner.
* **`ctx` (InvocationContext):** Provides access to crucial runtime information, most importantly `ctx.session.state`, which is the primary way to share data between steps orchestrated by your custom agent.

**TypeScript** — The heart of any custom agent is the `runAsyncImpl` method.

* **Signature:** `async* runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event, void, undefined>`
* **Asynchronous Generator:** It must be an `async` generator function (`async*`).
* **`ctx` (InvocationContext):** Provides access to crucial runtime information, most importantly `ctx.session.state`, which is the primary way to share data between steps orchestrated by your custom agent.

**Go** — You implement the `Run` method as part of a struct that satisfies the `agent.Agent` interface.

* **Signature:** `Run(ctx agent.InvocationContext) iter.Seq2[*session.Event, error]`
* **Iterator:** The `Run` method returns an iterator (`iter.Seq2`) that yields events and errors. This is the standard way to handle streaming results from an agent's execution.
* **`ctx` (InvocationContext):** The `agent.InvocationContext` provides access to the session, including state, and other crucial runtime information.
* **Session State:** You can access the session state through `ctx.Session().State()`.

**Java** — The heart of any custom agent is the `runAsyncImpl` method, which you override from `BaseAgent`.

* **Signature:** `protected Flowable<Event> runAsyncImpl(InvocationContext ctx)`
* **Reactive Stream (`Flowable`):** It must return an `io.reactivex.rxjava3.core.Flowable<Event>`. This `Flowable` represents a stream of events produced by the custom agent's logic, often by combining or transforming multiple `Flowable` from sub-agents.
* **`ctx` (InvocationContext):** Provides access to crucial runtime information, most importantly `ctx.session().state()`, which is a `java.util.concurrent.ConcurrentMap<String, Object>`. This is the primary way to share data between steps orchestrated by your custom agent.

**Key Capabilities within the Core Asynchronous Method:**

1. **Calling Sub-Agents:** You invoke sub-agents (stored as instance attributes like `self.my_llm_agent`) using their async run method and yield their events back to the runner. In Java, sub-agent `Flowable` streams are chained with operators like `concatWith`, `flatMapPublisher`, or `concatArray`. Use `Flowable.defer()` for subsequent stages when their execution depends on completion or state changes from prior stages.

2. **Managing State:** Read from and write to the session state (`ctx.session.state` in Python/TypeScript, `ctx.Session().State()` in Go, `ctx.session().state()` in Java) to pass data between sub-agent calls or make decisions. Decisions based on state values are how you implement conditional routing.

3. **Implementing Control Flow:** Use standard language constructs (`if`/`elif`/`else`, `for`/`while` loops, `try`/`except` or equivalents) to create sophisticated, conditional, or iterative workflows. In Java, use reactive operators: `Flowable.defer()` to choose which `Flowable` to subscribe to based on a condition, `repeat()`/`retry()` for iterative patterns.

> *Code examples: see [custom-agents-python.md](custom-agents-python.md), [custom-agents-typescript.md](custom-agents-typescript.md), [custom-agents-go.md](custom-agents-go.md), [custom-agents-java.md](custom-agents-java.md)*

## Managing Sub-Agents and State

Typically, a custom agent orchestrates other agents (like `LlmAgent`, `LoopAgent`, etc.).

* **Initialization:** You usually pass instances of these sub-agents into your custom agent's constructor and store them as instance fields/attributes (e.g., `self.story_generator = story_generator_instance`). This makes them accessible within the custom agent's core asynchronous execution logic.
* **Sub Agents List:** When initializing the `BaseAgent` using its `super()` constructor, you should pass a `sub_agents` list. This list tells the ADK framework about the agents that are part of this custom agent's immediate hierarchy. It's important for framework features like lifecycle management and introspection, even if your core execution logic calls the agents directly via instance attributes. Include the agents that your custom logic directly invokes at the top level.
* **State:** `ctx.session.state` is the standard way sub-agents (especially `LlmAgent`s using `output_key`) communicate results back to the orchestrator and how the orchestrator passes necessary inputs down.

## Design Pattern Example: `StoryFlowAgent`

Let's illustrate the power of custom agents with an example pattern: a multi-stage content generation workflow with conditional logic.

**Goal:** Create a system that generates a story, iteratively refines it through critique and revision, performs final checks, and crucially, *regenerates the story if the final tone check fails*.

**Why Custom?** The core requirement driving the need for a custom agent here is the **conditional regeneration based on the tone check**. Standard workflow agents don't have built-in conditional branching based on the outcome of a sub-agent's task. We need custom logic (`if tone == "negative": ...`) within the orchestrator.

---

### Part 1: Simplified Custom Agent Initialization

We define the `StoryFlowAgent` inheriting from `BaseAgent`. In the constructor, we store the necessary sub-agents (passed in) as instance attributes and tell the `BaseAgent` framework about the top-level agents this custom agent will directly orchestrate.

The key steps are:

1. Create any internal composite agents (like `LoopAgent` or `SequentialAgent`) before calling `super().__init__`.
2. Pass the list of all top-level sub-agents to the `super()` constructor via `sub_agents`.
3. Store the sub-agents as instance properties/attributes so they can be accessed in the custom run logic.

In Python, Pydantic is used for field declarations — sub-agent types must be declared as class attributes with type hints, and `model_config = {"arbitrary_types_allowed": True}` is required.

In Go, the pattern differs from class-based languages: you define a struct with the sub-agent fields and a constructor function (`NewStoryFlowAgent`) that returns an `agent.Agent` via `agent.New(...)`, passing the struct's `Run` method as the `Run` config field.

> *Code examples: see [custom-agents-python.md](custom-agents-python.md), [custom-agents-typescript.md](custom-agents-typescript.md), [custom-agents-go.md](custom-agents-go.md), [custom-agents-java.md](custom-agents-java.md)*

---

### Part 2: Defining the Custom Execution Logic

This is where the conditional orchestration happens. The method sequences the sub-agents and branches based on session state.

**Explanation of Logic:**

1. The initial `story_generator` runs. Its output is expected to be in `ctx.session.state["current_story"]`. If this key is absent or empty, the workflow aborts early.
2. The `loop_agent` runs, which internally calls the `critic` and `reviser` sequentially for `max_iterations` times. They read/write `current_story` and `criticism` from/to the state.
3. The `sequential_agent` runs, calling `grammar_check` then `tone_check`, reading `current_story` and writing `grammar_suggestions` and `tone_check_result` to the state.
4. **Custom Part:** The code checks the `tone_check_result` from the state. If it's `"negative"`, the `story_generator` is called *again*, overwriting `current_story` in the state. Otherwise, the flow ends.

In Java (RxJava), `Flowable.defer()` is the key operator for lazy conditional execution: each stage is wrapped in `defer` so its decision logic runs only after the prior stage completes. All stages are chained with `Flowable.concatArray(storyGenFlow, criticReviserFlow, postProcessingFlow, conditionalRegenFlow)`.

In TypeScript, `runLiveImpl` is also implemented and simply delegates to `runAsyncImpl` to handle live streaming scenarios.

> *Code examples: see [custom-agents-python.md](custom-agents-python.md), [custom-agents-typescript.md](custom-agents-typescript.md), [custom-agents-go.md](custom-agents-go.md), [custom-agents-java.md](custom-agents-java.md)*

---

### Part 3: Defining the LLM Sub-Agents

These are standard `LlmAgent` definitions, responsible for specific tasks. Their `output_key` parameter is crucial for placing results into `session.state` where other agents or the custom orchestrator can access them.

> **Direct State Injection in Instructions:** The `{var}` syntax in agent instructions is a placeholder. Before the instruction is sent to the LLM, the ADK framework automatically replaces `{topic}` (for example) with the value of `session.state['topic']`. This is the recommended way to provide context to an agent using instruction templating.

The sub-agents and their `output_key` assignments:

| Agent | `output_key` | Purpose |
|---|---|---|
| `StoryGenerator` | `current_story` | Generates the initial story from `{topic}` |
| `Critic` | `criticism` | Reviews `{current_story}`, outputs critique |
| `Reviser` | `current_story` | Revises story using `{criticism}` (overwrites) |
| `GrammarCheck` | `grammar_suggestions` | Checks grammar of `{current_story}` |
| `ToneCheck` | `tone_check_result` | Outputs `positive`, `negative`, or `neutral` |

The `ToneCheck` agent's single-word output drives the conditional logic in the custom orchestrator. In Java, the `LoopAgent` and `SequentialAgent` are also constructed at this stage before being passed to the `StoryFlowAgentExample` constructor.

> *Code examples: see [custom-agents-python.md](custom-agents-python.md), [custom-agents-typescript.md](custom-agents-typescript.md), [custom-agents-go.md](custom-agents-go.md), [custom-agents-java.md](custom-agents-java.md)*

---

### Part 4: Instantiating and Running the Custom Agent

Finally, you instantiate your `StoryFlowAgent` and use the `Runner` as usual. The initial session state must include the `"topic"` key that the `StoryGenerator` instruction references. The topic can be overwritten in session state before each run to vary the input.

> *Code examples: see [custom-agents-python.md](custom-agents-python.md), [custom-agents-typescript.md](custom-agents-typescript.md), [custom-agents-go.md](custom-agents-go.md), [custom-agents-java.md](custom-agents-java.md)*

---

## Full Code Example

Complete, self-contained runnable examples combining all parts of the `StoryFlowAgent` are available in the language sidecar files.

> *Code examples: see [custom-agents-python.md](custom-agents-python.md), [custom-agents-typescript.md](custom-agents-typescript.md), [custom-agents-go.md](custom-agents-go.md), [custom-agents-java.md](custom-agents-java.md)*
