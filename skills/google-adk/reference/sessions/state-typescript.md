# Session State — TypeScript Examples

## 1. `{key}` Templating in `LlmAgent` Instructions

Inject session state values directly into an agent's instruction string using `{key}` placeholders.

```typescript
import { LlmAgent } from "@google/adk";

const storyGenerator = new LlmAgent({
    name: "StoryGenerator",
    model: "gemini-2.5-flash",
    instruction: "Write a short story about a cat, focusing on the theme: {topic}."
});

// Assuming session.state['topic'] is set to "friendship", the LLM
// will receive the following instruction:
// "Write a short story about a cat, focusing on the theme: friendship."

// Use {topic?} for an optional key that may not be present:
const optionalGenerator = new LlmAgent({
    name: "OptionalStoryGenerator",
    model: "gemini-2.5-flash",
    instruction: "Write a short story about a cat, focusing on the theme: {topic?}."
});
```

## 2. `InstructionProvider` Function — Literal Curly Braces

When instructions contain literal curly braces (e.g., JSON examples), use an `InstructionProvider`
function instead of a string. The ADK will not attempt state injection; the string is passed as-is.

```typescript
import { LlmAgent, ReadonlyContext } from "@google/adk";

// This is an InstructionProvider
function myInstructionProvider(context: ReadonlyContext): string {
    // No state injection occurs — curly braces are treated as literal text.
    return 'Format your output as JSON: {"city": "<name>", "population": <number>}';
}

const agent = new LlmAgent({
    model: "gemini-2.5-flash",
    name: "template_helper_agent",
    instruction: myInstructionProvider
});
```

## 3. `inject_session_state` Utility with `InstructionProvider`

TypeScript does not expose a direct `inject_session_state` utility in the public API at the time
of writing. Use an `InstructionProvider` and access `context.state` manually to build dynamic
instructions while preserving literal curly braces.

```typescript
import { LlmAgent, ReadonlyContext } from "@google/adk";

function myDynamicInstructionProvider(context: ReadonlyContext): string {
    const adjective = context.state.get("adjective") ?? "dynamic";
    // Build the string manually to preserve literal braces for JSON examples.
    return `This is a ${adjective} instruction. Use JSON like: {"key": "value"}.`;
}

const agent = new LlmAgent({
    model: "gemini-2.5-flash",
    name: "dynamic_template_helper_agent",
    instruction: myDynamicInstructionProvider
});
```

## 4. `outputKey` → `getSession()` → `state` Round-Trip

The simplest way to persist an agent's text response into state. The `Runner` uses `outputKey`
to create the `stateDelta` automatically via `appendEvent`.

```typescript
import { LlmAgent, Runner, InMemorySessionService, isFinalResponse } from "@google/adk";
import { Content } from "@google/genai";

// Define agent with outputKey
const greetingAgent = new LlmAgent({
    name: "Greeter",
    model: "gemini-2.5-flash",
    instruction: "Generate a short, friendly greeting.",
    outputKey: "last_greeting"  // Saves final response text to state['last_greeting']
});

// --- Setup Runner and Session ---
const appName = "state_app";
const userId = "user1";
const sessionId = "session1";
const sessionService = new InMemorySessionService();
const runner = new Runner({
    agent: greetingAgent,
    appName,
    sessionService
});
const session = await sessionService.createSession({ appName, userId, sessionId });
console.log(`Initial state: ${JSON.stringify(session.state)}`);

// --- Run the Agent ---
const userMessage: Content = { parts: [{ text: "Hello" }] };
for await (const event of runner.runAsync({ userId, sessionId, newMessage: userMessage })) {
    if (isFinalResponse(event)) {
        console.log("Agent responded.");  // Response text is also in event.content
    }
}

// --- Check Updated State ---
const updatedSession = await sessionService.getSession({ appName, userId, sessionId });
console.log(`State after agent run: ${JSON.stringify(updatedSession?.state)}`);
// Expected: {"last_greeting":"Hello there! How can I help you today?"}
const greeting = updatedSession?.state["last_greeting"];
console.log(`Saved greeting: ${greeting}`);
```

## 5. `EventActions` `stateDelta` — Manual State Update via `appendEvent`

For complex updates: multiple keys, non-string values, scoped prefixes (`user:`, `app:`, `temp:`),
or updates not tied to an agent's final text response.

```typescript
import { InMemorySessionService, createEvent, createEventActions } from "@google/adk";

// --- Setup ---
const sessionService = new InMemorySessionService();
const appName = "state_app_manual";
const userId = "user2";
const sessionId = "session2";
const session = await sessionService.createSession({
    appName,
    userId,
    sessionId,
    state: { "user:login_count": 0, "task_status": "idle" }
});
console.log(`Initial state: ${JSON.stringify(session.state)}`);

// --- Define State Changes ---
const currentTime = Date.now();
const stateChanges = {
    "task_status": "active",                                                          // session-scoped
    "user:login_count": ((session.state["user:login_count"] as number) || 0) + 1,    // user-scoped
    "user:last_login_ts": currentTime,                                                // user-scoped
    "temp:validation_needed": true                                                    // temp (discarded after invocation)
};

// --- Create Event with Actions ---
const actionsWithUpdate = createEventActions({ stateDelta: stateChanges });
const systemEvent = createEvent({
    invocationId: "inv_login_update",
    author: "system",
    actions: actionsWithUpdate,
    timestamp: currentTime
});

// --- Append the Event (this updates the state) ---
await sessionService.appendEvent({ session, event: systemEvent });
console.log("`appendEvent` called with explicit state delta.");

// --- Check Updated State ---
const updatedSession = await sessionService.getSession({ appName, userId, sessionId });
console.log(`State after event: ${JSON.stringify(updatedSession?.state)}`);
// Expected: {"user:login_count":1,"task_status":"active","user:last_login_ts":<timestamp>}
// Note: 'temp:validation_needed' is NOT present (discarded after invocation).
```

## 6. `Context` State Mutation (Callbacks and Tools)

In TypeScript, both callback and tool contexts use the unified `Context` type. Changes to
`context.state` are automatically captured into the event's `stateDelta`.

```typescript
import { Context } from "@google/adk";

function myCallbackOrToolFunction(
    context: Context,
    // ... other parameters ...
): void {
    // Read then update an existing state value
    const count = (context.state.get("user_action_count") as number) ?? 0;
    context.state.set("user_action_count", count + 1);

    // Add a temporary value (discarded after the invocation ends)
    context.state.set("temp:last_operation_status", "success");

    // Changes are automatically part of the event's stateDelta —
    // no manual EventActions construction needed.
    // ... rest of callback/tool logic ...
}
```
