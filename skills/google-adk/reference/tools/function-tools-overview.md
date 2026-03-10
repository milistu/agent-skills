# Function Tools

Supported in ADK: Python v0.1.0, TypeScript v0.2.0, Go v0.1.0, Java v0.1.0

When pre-built ADK tools don't meet your requirements, you can create custom *function tools*. Building function tools allows you to create tailored functionality, such as connecting to proprietary databases or implementing unique algorithms.
For example, a function tool, `myfinancetool`, might be a function that calculates a specific financial metric. ADK also supports long-running functions, so if that calculation takes a while, the agent can continue working on other tasks.

ADK offers several ways to create function tools, each suited to different levels of complexity and control:

* Function Tools
* Long Running Function Tools
* Agents-as-a-Tool

## Function Tools

Transforming a Python function into a tool is a straightforward way to integrate custom logic into your agents. When you assign a function to an agent's `tools` list, the framework automatically wraps it as a `FunctionTool`.

### How it Works

The ADK framework automatically inspects your Python function's signature—including its name, docstring, parameters, type hints, and default values—to generate a schema. This schema is what the LLM uses to understand the tool's purpose, when to use it, and what arguments it requires.

### Defining Function Signatures

A well-defined function signature is crucial for the LLM to use your tool correctly.

#### Parameters

##### Required Parameters

A parameter is considered **required** if it has a type hint but **no default value**. The LLM must provide a value for this argument when it calls the tool. The parameter's description is taken from the function's docstring.

In this example, both `city` and `unit` are mandatory. If the LLM tries to call `get_weather` without one of them, the ADK will return an error to the LLM, prompting it to correct the call.

In Go, you use struct tags to control the JSON schema. The two primary tags are `json` and `jsonschema`.

A parameter is considered **required** in Go if its struct field does **not** have the `omitempty` or `omitzero` option in its `json` tag.

The `jsonschema` tag is used to provide the argument's description. This is crucial for the LLM to understand what the argument is for.

> *Code examples: see [function-tools-overview-python.md](function-tools-overview-python.md), [function-tools-overview-typescript.md](function-tools-overview-typescript.md), [function-tools-overview-go.md](function-tools-overview-go.md), [function-tools-overview-java.md](function-tools-overview-java.md)*

##### Optional Parameters

A parameter is considered **optional** in Python if you provide a **default value**. This is the standard Python way to define optional arguments. You can also mark a parameter as optional using `typing.Optional[SomeType]` or the `| None` syntax (Python 3.10+).

In Go, a parameter is considered **optional** if its struct field has the `omitempty` or `omitzero` option in its `json` tag.

> *Code examples: see [function-tools-overview-python.md](function-tools-overview-python.md), [function-tools-overview-typescript.md](function-tools-overview-typescript.md), [function-tools-overview-go.md](function-tools-overview-go.md), [function-tools-overview-java.md](function-tools-overview-java.md)*

##### Optional Parameters with `typing.Optional`

You can also mark a parameter as optional using `typing.Optional[SomeType]` or the `| None` syntax (Python 3.10+). This signals that the parameter can be `None`. When combined with a default value of `None`, it behaves as a standard optional parameter.

> *Code examples: see [function-tools-overview-python.md](function-tools-overview-python.md), [function-tools-overview-typescript.md](function-tools-overview-typescript.md), [function-tools-overview-go.md](function-tools-overview-go.md), [function-tools-overview-java.md](function-tools-overview-java.md)*

##### Variadic Parameters (`*args` and `**kwargs`)

While you can include `*args` (variable positional arguments) and `**kwargs` (variable keyword arguments) in your function signature for other purposes, they are **ignored by the ADK framework** when generating the tool schema for the LLM. The LLM will not be aware of them and cannot pass arguments to them. It's best to rely on explicitly defined parameters for all data you expect from the LLM.

#### Return Type

The preferred return type for a Function Tool is a **dictionary** in Python, a **Map** in Java, or an **object** in TypeScript. This allows you to structure the response with key-value pairs, providing context and clarity to the LLM. If your function returns a type other than a dictionary, the framework automatically wraps it into a dictionary with a single key named **"result"**.

Strive to make your return values as descriptive as possible. *For example,* instead of returning a numeric error code, return a dictionary with an "error\_message" key containing a human-readable explanation. **Remember that the LLM**, not a piece of code, needs to understand the result. As a best practice, include a "status" key in your return dictionary to indicate the overall outcome (e.g., "success", "error", "pending"), providing the LLM with a clear signal about the operation's state.

#### Docstrings

The docstring of your function serves as the tool's **description** and is sent to the LLM. Therefore, a well-written and comprehensive docstring is crucial for the LLM to understand how to use the tool effectively. Clearly explain the purpose of the function, the meaning of its parameters, and the expected return values.

### Passing Data Between Tools

When an agent calls multiple tools in a sequence, you might need to pass data from one tool to another. The recommended way to do this is by using the `temp:` prefix in the session state.

A tool can write data to a `temp:` variable, and a subsequent tool can read it. This data is only available for the current invocation and is discarded afterwards.

> **Shared Invocation Context:** All tool calls within a single agent turn share the same `InvocationContext`. This means they also share the same temporary (`temp:`) state, which is how data can be passed between them.

### Example

This tool is a Python function which obtains the stock price of a given stock ticker/symbol.

Note: You need to install the `yfinance` library before using the Python example (`pip install yfinance`).

The return value from a function that returns a non-dict type will be wrapped into a dictionary: `{"result": "$123"}`.

> *Code examples: see [function-tools-overview-python.md](function-tools-overview-python.md), [function-tools-overview-typescript.md](function-tools-overview-typescript.md), [function-tools-overview-go.md](function-tools-overview-go.md), [function-tools-overview-java.md](function-tools-overview-java.md)*

### Best Practices

While you have considerable flexibility in defining your function, remember that simplicity enhances usability for the LLM. Consider these guidelines:

* **Fewer Parameters are Better:** Minimize the number of parameters to reduce complexity.
* **Simple Data Types:** Favor primitive data types like `str` and `int` over custom classes whenever possible.
* **Meaningful Names:** The function's name and parameter names significantly influence how the LLM interprets and utilizes the tool. Choose names that clearly reflect the function's purpose and the meaning of its inputs. Avoid generic names like `do_stuff()` or `beAgent()`.
* **Build for Parallel Execution:** Improve function calling performance when multiple tools are run by building for asynchronous operation.

## Long Running Function Tools

This tool is designed to help you start and manage tasks that are handled outside the operation of your agent workflow, and require a significant amount of processing time, without blocking the agent's execution. This tool is a subclass of `FunctionTool`.

When using a `LongRunningFunctionTool`, your function can initiate the long-running operation and optionally return an **initial result**, such as a long-running operation id. Once a long running function tool is invoked the agent runner pauses the agent run and lets the agent client decide whether to continue or wait until the long-running operation finishes. The agent client can query the progress of the long-running operation and send back an intermediate or final response. The agent can then continue with other tasks. An example is the human-in-the-loop scenario where the agent needs human approval before proceeding with a task.

> **Warning: Execution handling**
>
> Long Running Function Tools are designed to help you start and *manage* long running tasks as part of your agent workflow, but ***not perform*** the actual, long task. For tasks that require significant time to complete, you should implement a separate server to do the task.

> **Tip: Parallel execution**
>
> Depending on the type of tool you are building, designing for asynchronous operation may be a better solution than creating a long running tool.

### How it Works

In Python, you wrap a function with `LongRunningFunctionTool`. In Java, you pass a Method name to `LongRunningFunctionTool.create()`. In TypeScript, you instantiate the `LongRunningFunctionTool` class.

1. **Initiation:** When the LLM calls the tool, your function starts the long-running operation.
2. **Initial Updates:** Your function should optionally return an initial result (e.g. the long-running operation id). The ADK framework takes the result and sends it back to the LLM packaged within a `FunctionResponse`. This allows the LLM to inform the user (e.g., status, percentage complete, messages). And then the agent run is ended / paused.
3. **Continue or Wait:** After each agent run is completed, the agent client can query the progress of the long-running operation and decide whether to continue the agent run with an intermediate response (to update the progress) or wait until a final response is retrieved. The agent client should send the intermediate or final response back to the agent for the next run.
4. **Framework Handling:** The ADK framework manages the execution. It sends the intermediate or final `FunctionResponse` sent by the agent client to the LLM to generate a user-friendly message.

### Creating the Tool

Define your tool function and wrap it using the `LongRunningFunctionTool` class:

> *Code examples: see [function-tools-overview-python.md](function-tools-overview-python.md), [function-tools-overview-typescript.md](function-tools-overview-typescript.md), [function-tools-overview-go.md](function-tools-overview-go.md), [function-tools-overview-java.md](function-tools-overview-java.md)*

### Intermediate / Final Result Updates

The agent client receives an event with long running function calls and checks the status of the ticket. Then the agent client can send the intermediate or final response back to update the progress. The framework packages this value (even if it's None) into the content of the `FunctionResponse` sent back to the LLM.

> **Note: Long running function response with Resume feature**
>
> If your ADK agent workflow is configured with the Resume feature, you also must include the Invocation ID (`invocation_id`) parameter with the long running function response. The Invocation ID you provide must be the same invocation that generated the long running function request, otherwise the system starts a new invocation with the response. If your agent uses the Resume feature, consider including the Invocation ID as a parameter with your long running function request, so it can be included with the response.

> **Applies to Java ADK only:** When passing `ToolContext` with Function Tools, ensure that one of the following is true:
>
> * The Schema annotation is passed with the ToolContext parameter in the function signature:
>   `@com.google.adk.tools.Annotations.Schema(name = "toolContext") ToolContext toolContext`
> * OR the `-parameters` flag is set in the Maven compiler plugin configuration (see the Java sidecar for the Maven XML snippet).
>
> This constraint is temporary and will be removed.

> *Code examples: see [function-tools-overview-python.md](function-tools-overview-python.md), [function-tools-overview-typescript.md](function-tools-overview-typescript.md), [function-tools-overview-go.md](function-tools-overview-go.md), [function-tools-overview-java.md](function-tools-overview-java.md)*

#### Key Aspects of the Long Running Example

* **`LongRunningFunctionTool`**: Wraps the supplied method/function; the framework handles sending yielded updates and the final return value as sequential FunctionResponses.
* **Agent instruction**: Directs the LLM to use the tool and understand the incoming FunctionResponse stream (progress vs. completion) for user updates.
* **Final return**: The function returns the final result dictionary, which is sent in the concluding FunctionResponse to indicate completion.

## Agent-as-a-Tool

This powerful feature allows you to leverage the capabilities of other agents within your system by calling them as tools. The Agent-as-a-Tool enables you to invoke another agent to perform a specific task, effectively **delegating responsibility**. This is conceptually similar to creating a Python function that calls another agent and uses the agent's response as the function's return value.

### Key Difference from Sub-Agents

It's important to distinguish an Agent-as-a-Tool from a Sub-Agent.

* **Agent-as-a-Tool:** When Agent A calls Agent B as a tool (using Agent-as-a-Tool), Agent B's answer is **passed back** to Agent A, which then summarizes the answer and generates a response to the user. Agent A retains control and continues to handle future user input.
* **Sub-agent:** When Agent A calls Agent B as a sub-agent, the responsibility of answering the user is completely **transferred to Agent B**. Agent A is effectively out of the loop. All subsequent user input will be answered by Agent B.

### Usage

To use an agent as a tool, wrap the agent with the `AgentTool` class.

> *Code examples: see [function-tools-overview-python.md](function-tools-overview-python.md), [function-tools-overview-typescript.md](function-tools-overview-typescript.md), [function-tools-overview-go.md](function-tools-overview-go.md), [function-tools-overview-java.md](function-tools-overview-java.md)*

### Customization

The `AgentTool` class provides the following attributes for customizing its behavior:

* **`skip_summarization: bool`:** If set to `True`, the framework will **bypass the LLM-based summarization** of the tool agent's response. This can be useful when the tool's response is already well-formatted and requires no further processing.

> *Code examples: see [function-tools-overview-python.md](function-tools-overview-python.md), [function-tools-overview-typescript.md](function-tools-overview-typescript.md), [function-tools-overview-go.md](function-tools-overview-go.md), [function-tools-overview-java.md](function-tools-overview-java.md)*

### How it Works

1. When the `main_agent` receives the long text, its instruction tells it to use the 'summarize' tool for long texts.
2. The framework recognizes 'summarize' as an `AgentTool` that wraps the `summary_agent`.
3. Behind the scenes, the `main_agent` will call the `summary_agent` with the long text as input.
4. The `summary_agent` will process the text according to its instruction and generate a summary.
5. **The response from the `summary_agent` is then passed back to the `main_agent`.**
6. The `main_agent` can then take the summary and formulate its final response to the user (e.g., "Here's a summary of the text: ...")
