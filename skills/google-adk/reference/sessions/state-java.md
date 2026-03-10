# Session State — Java Examples

> **Note:** The source documentation does not provide Java examples for `{key}` templating in
> instructions or for the `InstructionProvider` / `inject_session_state` patterns. Those features
> may be available in the Java SDK — consult the Java API reference for details. The examples
> below cover the patterns that are explicitly documented with Java code.

## 1. `outputKey` → `getSession()` → `state()` Round-Trip

The simplest way to persist an agent's text response into state. The `Runner` uses `outputKey`
to create the `stateDelta` automatically via `appendEvent`.

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.RunConfig;
import com.google.adk.events.Event;
import com.google.adk.runner.Runner;
import com.google.adk.sessions.InMemorySessionService;
import com.google.adk.sessions.Session;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import java.util.List;
import java.util.Optional;

public class GreetingAgentExample {

    public static void main(String[] args) {
        // Define agent with outputKey — saves final response text to state["last_greeting"]
        LlmAgent greetingAgent = LlmAgent.builder()
                .name("Greeter")
                .model("gemini-2.0-flash")
                .instruction("Generate a short, friendly greeting.")
                .description("Greeting agent")
                .outputKey("last_greeting")
                .build();

        // --- Setup Runner and Session ---
        String appName = "state_app";
        String userId = "user1";
        String sessionId = "session1";

        InMemorySessionService sessionService = new InMemorySessionService();
        Runner runner = new Runner(greetingAgent, appName, null, sessionService);

        Session session = sessionService.createSession(appName, userId, null, sessionId)
                .blockingGet();
        System.out.println("Initial state: " + session.state().entrySet());

        // --- Run the Agent ---
        Content userMessage = Content.builder()
                .parts(List.of(Part.fromText("Hello")))
                .build();
        RunConfig runConfig = RunConfig.builder().build();

        for (Event event : runner.runAsync(userId, sessionId, userMessage, runConfig)
                .blockingIterable()) {
            if (event.finalResponse()) {
                System.out.println("Agent responded.");
            }
        }

        // --- Check Updated State ---
        Session updatedSession = sessionService
                .getSession(appName, userId, sessionId, Optional.empty())
                .blockingGet();
        assert updatedSession != null;
        System.out.println("State after agent run: " + updatedSession.state().entrySet());
        // Expected: {last_greeting=Hello there! How can I help you today?}
        Object greeting = updatedSession.state().get("last_greeting");
        System.out.println("Saved greeting: " + greeting);
    }
}
```

## 2. `EventActions.stateDelta` — Manual State Update via `appendEvent`

For complex updates: multiple keys, non-string values, scoped prefixes (`user:`, `app:`, `temp:`),
or updates not tied to an agent's final text response.

```java
import com.google.adk.events.Event;
import com.google.adk.events.EventActions;
import com.google.adk.sessions.InMemorySessionService;
import com.google.adk.sessions.Session;
import java.time.Instant;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

public class ManualStateUpdateExample {

    public static void main(String[] args) {
        // --- Setup ---
        InMemorySessionService sessionService = new InMemorySessionService();
        String appName = "state_app_manual";
        String userId = "user2";
        String sessionId = "session2";

        ConcurrentMap<String, Object> initialState = new ConcurrentHashMap<>();
        initialState.put("user:login_count", 0);
        initialState.put("task_status", "idle");

        Session session = sessionService.createSession(appName, userId, initialState, sessionId)
                .blockingGet();
        System.out.println("Initial state: " + session.state().entrySet());

        // --- Define State Changes ---
        long currentTimeMillis = Instant.now().toEpochMilli();

        ConcurrentMap<String, Object> stateChanges = new ConcurrentHashMap<>();
        stateChanges.put("task_status", "active");                    // session-scoped

        Object loginCountObj = session.state().get("user:login_count");
        int currentLoginCount = 0;
        if (loginCountObj instanceof Number) {
            currentLoginCount = ((Number) loginCountObj).intValue();
        }
        stateChanges.put("user:login_count", currentLoginCount + 1);  // user-scoped
        stateChanges.put("user:last_login_ts", currentTimeMillis);     // user-scoped
        stateChanges.put("temp:validation_needed", true);              // temp (discarded after invocation)

        // --- Create Event with Actions ---
        EventActions actionsWithUpdate = EventActions.builder()
                .stateDelta(stateChanges)
                .build();

        Event systemEvent = Event.builder()
                .invocationId("inv_login_update")
                .author("system")
                .actions(actionsWithUpdate)
                .timestamp(currentTimeMillis)
                .build();

        // --- Append the Event (this updates the state) ---
        sessionService.appendEvent(session, systemEvent).blockingGet();
        System.out.println("`appendEvent` called with explicit state delta.");

        // --- Check Updated State ---
        Session updatedSession = sessionService
                .getSession(appName, userId, sessionId, Optional.empty())
                .blockingGet();
        assert updatedSession != null;
        System.out.println("State after event: " + updatedSession.state().entrySet());
        // Expected: {user:login_count=1, task_status=active, user:last_login_ts=<timestamp_millis>}
        // Note: 'temp:validation_needed' is NOT present (discarded after invocation).
    }
}
```

## 3. `CallbackContext` State Mutation (Callbacks and Tools)

The recommended way to mutate state from within agent callbacks or tool methods. Changes made via
`callbackContext.state()` are automatically captured into the event's `stateDelta`.

```java
import com.google.adk.agents.CallbackContext; // or ToolContext for tools

public class MyAgentCallbacks {

    public void onAfterAgent(CallbackContext callbackContext) {
        // Read then update an existing state value
        Integer count = (Integer) callbackContext.state().getOrDefault("user_action_count", 0);
        callbackContext.state().put("user_action_count", count + 1);

        // Add a temporary value (discarded after the invocation ends)
        callbackContext.state().put("temp:last_operation_status", "success");

        // Changes are automatically part of the event's stateDelta —
        // no manual EventActions construction needed.
        // ... rest of callback logic ...
    }
}
```
