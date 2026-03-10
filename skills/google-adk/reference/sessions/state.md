# State: The Session's Scratchpad

Within each `Session` (our conversation thread), the **`state`** attribute acts like the agent's dedicated scratchpad for that specific interaction. While `session.events` holds the full history, `session.state` is where the agent stores and updates dynamic details needed *during* the conversation.

## What is `session.state`?

Conceptually, `session.state` is a collection (dictionary or Map) holding key-value pairs. It's designed for information the agent needs to recall or track to make the current conversation effective:

* **Personalize Interaction:** Remember user preferences mentioned earlier (e.g., `'user_preference_theme': 'dark'`).
* **Track Task Progress:** Keep tabs on steps in a multi-turn process (e.g., `'booking_step': 'confirm_payment'`).
* **Accumulate Information:** Build lists or summaries (e.g., `'shopping_cart_items': ['book', 'pen']`).
* **Make Informed Decisions:** Store flags or values influencing the next response (e.g., `'user_is_authenticated': True`).

### Key Characteristics of `State`

1. **Structure: Serializable Key-Value Pairs**

   * Data is stored as `key: value`.
   * **Keys:** Always strings (`str`). Use clear names (e.g., `'departure_city'`, `'user:language_preference'`).
   * **Values:** Must be **serializable**. This means they can be easily saved and loaded by the `SessionService`. Stick to basic types in the specific languages (Python/Go/Java/TypeScript) like strings, numbers, booleans, and simple lists or dictionaries containing *only* these basic types. (See API documentation for precise details).
   * **Avoid Complex Objects:** **Do not store non-serializable objects** (custom class instances, functions, connections, etc.) directly in the state. Store simple identifiers if needed, and retrieve the complex object elsewhere.

2. **Mutability: It Changes**

   * The contents of the `state` are expected to change as the conversation evolves.

3. **Persistence: Depends on `SessionService`**

   * Whether state survives application restarts depends on your chosen service:
   * `InMemorySessionService`: **Not Persistent.** State is lost on restart.
   * `DatabaseSessionService` / `VertexAiSessionService`: **Persistent.** State is saved reliably.

> **Note:** The specific parameters or method names for the primitives may vary slightly by SDK language (e.g., `session.state['current_intent'] = 'book_flight'` in Python, `context.State().Set("current_intent", "book_flight")` in Go, `session.state().put("current_intent", "book_flight")` in Java, or `context.state.set("current_intent", "book_flight")` in TypeScript). Refer to the language-specific API documentation for details.

### Organizing State with Prefixes: Scope Matters

Prefixes on state keys define their scope and persistence behavior, especially with persistent services:

* **No Prefix (Session State):**

  + **Scope:** Specific to the *current* session (`id`).
  + **Persistence:** Only persists if the `SessionService` is persistent (`Database`, `VertexAI`).
  + **Use Cases:** Tracking progress within the current task (e.g., `'current_booking_step'`), temporary flags for this interaction (e.g., `'needs_clarification'`).
  + **Example:** `session.state['current_intent'] = 'book_flight'`

* **`user:` Prefix (User State):**

  + **Scope:** Tied to the `user_id`, shared across *all* sessions for that user (within the same `app_name`).
  + **Persistence:** Persistent with `Database` or `VertexAI`. (Stored by `InMemory` but lost on restart).
  + **Use Cases:** User preferences (e.g., `'user:theme'`), profile details (e.g., `'user:name'`).
  + **Example:** `session.state['user:preferred_language'] = 'fr'`

* **`app:` Prefix (App State):**

  + **Scope:** Tied to the `app_name`, shared across *all* users and sessions for that application.
  + **Persistence:** Persistent with `Database` or `VertexAI`. (Stored by `InMemory` but lost on restart).
  + **Use Cases:** Global settings (e.g., `'app:api_endpoint'`), shared templates.
  + **Example:** `session.state['app:global_discount_code'] = 'SAVE10'`

* **`temp:` Prefix (Temporary Invocation State):**

  + **Scope:** Specific to the current **invocation** (the entire process from an agent receiving user input to generating the final output for that input).
  + **Persistence:** **Not Persistent.** Discarded after the invocation completes and does not carry over to the next one.
  + **Use Cases:** Storing intermediate calculations, flags, or data passed between tool calls within a single invocation.
  + **When Not to Use:** For information that must persist across different invocations, such as user preferences, conversation history summaries, or accumulated data.
  + **Example:** `session.state['temp:raw_api_response'] = {...}`

> **Sub-Agents and Invocation Context:** When a parent agent calls a sub-agent (e.g., using `SequentialAgent` or `ParallelAgent`), it passes its `InvocationContext` to the sub-agent. This means the entire chain of agent calls shares the same invocation ID and, therefore, the same `temp:` state.

**How the Agent Sees It:** Your agent code interacts with the *combined* state through the single `session.state` collection (dict/Map). The `SessionService` handles fetching/merging state from the correct underlying storage based on prefixes.

### Accessing Session State in Agent Instructions

When working with `LlmAgent` instances, you can directly inject session state values into the agent's instruction string using a simple templating syntax. This allows you to create dynamic and context-aware instructions without relying solely on natural language directives.

#### Using `{key}` Templating

To inject a value from the session state, enclose the key of the desired state variable within curly braces: `{key}`. The framework will automatically replace this placeholder with the corresponding value from `session.state` before passing the instruction to the LLM.

> *Code examples: see [state-python.md](state-python.md), [state-typescript.md](state-typescript.md), [state-go.md](state-go.md), [state-java.md](state-java.md)*

#### Important Considerations

* **Key Existence:** Ensure that the key you reference in the instruction string exists in `session.state`. If the key is missing, the agent will throw an error. To use a key that may or may not be present, you can include a question mark (`?`) after the key (e.g. `{topic?}`).
* **Data Types:** The value associated with the key should be a string or a type that can be easily converted to a string.
* **Literal Curly Braces:** The `{key}` syntax matches any valid Python identifier inside single curly braces. If you need literal curly braces in your instruction, such as for JSON formatting or templating syntax, use an `InstructionProvider` function instead of a string (see below).

> **f-strings and double braces:** Some ADK examples use Python f-strings in instructions, such as `f"Topic: {{initial_topic}}"`. The `{{` and `}}` in those examples are **Python f-string escaping**, not ADK syntax. At runtime, Python converts `{{initial_topic}}` to `{initial_topic}`, which ADK then treats as a normal state variable placeholder. If you are not using f-strings, use single braces `{key}` directly.

#### Using `InstructionProvider` for Full Control

In some cases, you may need full control over the instruction string — for example, when your instructions contain literal curly braces (e.g., JSON examples, templating syntax) that would otherwise be interpreted as state variable placeholders.

To achieve this, provide a function to the `instruction` parameter instead of a string. This function is called an `InstructionProvider`. When you use an `InstructionProvider`, the ADK will **not** attempt to inject state variables, and the returned string will be passed to the model as-is.

The `InstructionProvider` function receives a `ReadonlyContext` object, which you can use to access session state or other contextual information if you need to build the instruction dynamically.

> *Code examples: see [state-python.md](state-python.md), [state-typescript.md](state-typescript.md), [state-go.md](state-go.md), [state-java.md](state-java.md)*

If you want to both use an `InstructionProvider` *and* inject state into your instructions, you can use the `inject_session_state` utility function. Only `{key}` placeholders matching valid state variable names will be replaced; other text (including curly braces that don't match valid identifiers) will be left as-is.

> *Code examples: see [state-python.md](state-python.md), [state-typescript.md](state-typescript.md), [state-go.md](state-go.md), [state-java.md](state-java.md)*

**Benefits of Direct Injection**

* **Clarity:** Makes it explicit which parts of the instruction are dynamic and based on session state.
* **Reliability:** Avoids relying on the LLM to correctly interpret natural language instructions to access state.
* **Maintainability:** Simplifies instruction strings and reduces the risk of errors when updating state variable names.

**Relation to Other State Access Methods**

This direct injection method is specific to `LlmAgent` instructions. Refer to the following section for more information on other state access methods.

### How State is Updated: Recommended Methods

> **The Right Way to Modify State:** When you need to change the session state, the correct and safest method is to **directly modify the `state` object on the `Context`** provided to your function (e.g., `callback_context.state['my_key'] = 'new_value'`). This is considered "direct state manipulation" in the right way, as the framework automatically tracks these changes.
>
> This is critically different from directly modifying the `state` on a `Session` object you retrieve from the `SessionService` (e.g., `my_session.state['my_key'] = 'new_value'`). **You should avoid this**, as it bypasses the ADK's event tracking and can lead to lost data. The warning section below has more details on this important distinction.

State should **always** be updated as part of adding an `Event` to the session history using `session_service.append_event()`. This ensures changes are tracked, persistence works correctly, and updates are thread-safe.

**1. The Easy Way: `output_key` (for Agent Text Responses)**

This is the simplest method for saving an agent's final text response directly into the state. When defining your `LlmAgent`, specify the `output_key`. Behind the scenes, the `Runner` uses the `output_key` to create the necessary `EventActions` with a `state_delta` and calls `append_event`.

> *Code examples: see [state-python.md](state-python.md), [state-typescript.md](state-typescript.md), [state-go.md](state-go.md), [state-java.md](state-java.md)*

**2. The Standard Way: `EventActions.state_delta` (for Complex Updates)**

For more complex scenarios (updating multiple keys, non-string values, specific scopes like `user:` or `app:`, or updates not tied directly to the agent's final text), you manually construct the `state_delta` within `EventActions`.

> *Code examples: see [state-python.md](state-python.md), [state-typescript.md](state-typescript.md), [state-go.md](state-go.md), [state-java.md](state-java.md)*

**3. Via `CallbackContext` or `ToolContext` (Recommended for Callbacks and Tools)**

*(Note: In TypeScript, this is done via the unified `Context` type.)*

Modifying state within agent callbacks (e.g., `on_before_agent_call`, `on_after_agent_call`) or tool functions is best done using the `state` attribute of the `CallbackContext` or `ToolContext` provided to your function.

* `callback_context.state['my_key'] = my_value`
* `tool_context.state['my_key'] = my_value`

These context objects are specifically designed to manage state changes within their respective execution scopes. When you modify `context.state`, the ADK framework ensures that these changes are automatically captured and correctly routed into the `EventActions.state_delta` for the event being generated by the callback or tool. This delta is then processed by the `SessionService` when the event is appended, ensuring proper persistence and tracking.

This method abstracts away the manual creation of `EventActions` and `state_delta` for most common state update scenarios within callbacks and tools, making your code cleaner and less error-prone.

For more comprehensive details on context objects, refer to the Context documentation.

> *Code examples: see [state-python.md](state-python.md), [state-typescript.md](state-typescript.md), [state-go.md](state-go.md), [state-java.md](state-java.md)*

**What `append_event` Does:**

* Adds the `Event` to `session.events`.
* Reads the `state_delta` from the event's `actions`.
* Applies these changes to the state managed by the `SessionService`, correctly handling prefixes and persistence based on the service type.
* Updates the session's `last_update_time`.
* Ensures thread-safety for concurrent updates.

### Warning: Direct State Modification

Avoid directly modifying the `session.state` collection (dictionary/Map) on a `Session` object that was obtained directly from the `SessionService` (e.g., via `session_service.get_session()` or `session_service.create_session()`) *outside* of the managed lifecycle of an agent invocation (i.e., not through a `CallbackContext` or `ToolContext`). For example, code like `retrieved_session = await session_service.get_session(...); retrieved_session.state['key'] = value` is problematic.

State modifications *within* callbacks or tools using `CallbackContext.state` or `ToolContext.state` are the correct way to ensure changes are tracked, as these context objects handle the necessary integration with the event system.

**Why direct modification (outside of contexts) is strongly discouraged:**

1. **Bypasses Event History:** The change isn't recorded as an `Event`, losing auditability.
2. **Breaks Persistence:** Changes made this way **will likely NOT be saved** by `DatabaseSessionService` or `VertexAiSessionService`. They rely on `append_event` to trigger saving.
3. **Not Thread-Safe:** Can lead to race conditions and lost updates.
4. **Ignores Timestamps/Logic:** Doesn't update `last_update_time` or trigger related event logic.

**Recommendation:** Stick to updating state via `output_key`, `EventActions.state_delta` (when manually creating events), or by modifying the `state` property of `CallbackContext` or `ToolContext` objects when within their respective scopes. These methods ensure reliable, trackable, and persistent state management. Use direct access to `session.state` (from a `SessionService`-retrieved session) only for *reading* state.

### Best Practices for State Design Recap

* **Minimalism:** Store only essential, dynamic data.
* **Serialization:** Use basic, serializable types.
* **Descriptive Keys & Prefixes:** Use clear names and appropriate prefixes (`user:`, `app:`, `temp:`, or none).
* **Shallow Structures:** Avoid deep nesting where possible.
* **Standard Update Flow:** Rely on `append_event`.
