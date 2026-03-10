# Memory Service — Java Examples

## 1. InMemoryMemoryService: addSessionToMemory, LoadMemoryTool, two-runner cross-session recall

```java
package com.google.adk.examples.sessions;

import com.google.adk.agents.LlmAgent;
import com.google.adk.memory.InMemoryMemoryService;
import com.google.adk.runner.Runner;
import com.google.adk.sessions.InMemorySessionService;
import com.google.adk.sessions.Session;
import com.google.adk.tools.LoadMemoryTool;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import java.util.Optional;

public class MemoryExample {

  private static final String APP_NAME = "memory_example_app";
  private static final String USER_ID = "mem_user";
  private static final String MODEL = "gemini-2.0-flash";

  public static void main(String[] args) {
    // Services must be shared across runners to share state and memory.
    InMemorySessionService sessionService = new InMemorySessionService();
    InMemoryMemoryService memoryService = new InMemoryMemoryService();

    // Agent 1: Capture
    LlmAgent infoCaptureAgent = new LlmAgent.Builder()
        .model(MODEL)
        .name("InfoCaptureAgent")
        .instruction("Acknowledge the user's statement.")
        .build();

    // Agent 2: Recall (has LoadMemoryTool)
    LlmAgent memoryRecallAgent = new LlmAgent.Builder()
        .model(MODEL)
        .name("MemoryRecallAgent")
        .instruction("Answer the user's question. Use the 'load_memory' tool "
            + "if the answer might be in past conversations.")
        .tools(new LoadMemoryTool())
        .build();

    // Turn 1: Capture information
    System.out.println("--- Turn 1: Capturing Information ---");
    Runner runner1 = new Runner.Builder()
        .agent(infoCaptureAgent)
        .appName(APP_NAME)
        .sessionService(sessionService)
        .memoryService(memoryService)
        .build();

    String session1Id = "session_info";
    sessionService.createSession(APP_NAME, USER_ID, null, session1Id).blockingGet();

    Content userInput1 = Content.fromParts(
        Part.fromText("My favorite project is Project Alpha."));

    runner1.runAsync(USER_ID, session1Id, userInput1)
        .blockingForEach(event -> {
          if (event.finalResponse() && event.content().isPresent()) {
            System.out.println("Agent 1 Response: "
                + event.content().get().parts().get(0).text().get());
          }
        });

    // Add session to memory
    System.out.println("\n--- Adding Session 1 to Memory ---");
    Session completedSession1 = sessionService
        .getSession(APP_NAME, USER_ID, session1Id, Optional.empty())
        .blockingGet();
    memoryService.addSessionToMemory(completedSession1).blockingAwait();
    System.out.println("Session added to memory.");

    // Turn 2: Recall in a new session
    System.out.println("\n--- Turn 2: Recalling Information ---");
    Runner runner2 = new Runner.Builder()
        .agent(memoryRecallAgent)
        .appName(APP_NAME)
        .sessionService(sessionService)
        .memoryService(memoryService)
        .build();

    String session2Id = "session_recall";
    sessionService.createSession(APP_NAME, USER_ID, null, session2Id).blockingGet();

    Content userInput2 = Content.fromParts(Part.fromText("What is my favorite project?"));

    runner2.runAsync(USER_ID, session2Id, userInput2)
        .blockingForEach(event -> {
          if (event.finalResponse() && event.content().isPresent()) {
            System.out.println("Agent 2 Response: "
                + event.content().get().parts().get(0).text().get());
          }
        });
  }
}
```

## 2. Searching Memory Within a Tool (via ToolContext)

```java
// Within a custom tool implementation
public Single<ToolOutput> execute(ToolContext context) {
  String query = ...; // get query from tool arguments
  return context.searchMemory(query)
      .map(response -> {
          // process response.memories()
          return new ToolOutput(response.memories().toString());
      });
}
```

## 3. LoadMemoryTool in tools + afterAgentCallback auto-save pattern

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.tools.LoadMemoryTool;
import io.reactivex.rxjava3.core.Maybe;

// Agent with LoadMemoryTool — retrieves memory when the agent decides it is needed
LlmAgent agent = new LlmAgent.Builder()
    .model(MODEL_ID)
    .name("weather_sentiment_agent")
    .instruction("...")
    .tools(new LoadMemoryTool())
    .build();
```

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.tools.LoadMemoryTool;
import io.reactivex.rxjava3.core.Maybe;

// afterAgentCallback auto-saves each completed session to memory
LlmAgent agent = new LlmAgent.Builder()
    .model(MODEL)
    .name("Generic_QA_Agent")
    .instruction("Answer the user's questions")
    .tools(new LoadMemoryTool())
    .afterAgentCallback((context) -> {
        return context.invocationContext().memoryService()
            .addSessionToMemory(context.invocationContext().session())
            .andThen(Maybe.empty());
    })
    .build();
```
