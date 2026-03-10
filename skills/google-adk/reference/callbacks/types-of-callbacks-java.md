# Callback Types — Java Examples

## before_agent_callback

Checks `skip_llm_agent` in session state. Returns `Maybe.just(Content)` to skip the agent, or `Maybe.empty()` to proceed.

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.CallbackContext;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.sessions.State;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class BeforeAgentCallbackExample {

  private static final String APP_NAME = "AgentWithBeforeAgentCallback";
  private static final String USER_ID = "test_user_456";
  private static final String SESSION_ID = "session_id_123";
  private static final String MODEL_NAME = "gemini-2.0-flash";

  public static void main(String[] args) {
    BeforeAgentCallbackExample callbackAgent = new BeforeAgentCallbackExample();
    callbackAgent.defineAgent("Write a document about a cat");
  }

  // Checks 'skip_llm_agent' in state. Returns Content to skip, or Maybe.empty() to proceed.
  public Maybe<Content> checkIfAgentShouldRun(CallbackContext callbackContext) {
    String agentName = callbackContext.agentName();
    String invocationId = callbackContext.invocationId();
    State currentState = callbackContext.state();

    System.out.printf("%n[Callback] Entering agent: %s (Inv: %s)%n", agentName, invocationId);
    System.out.printf("[Callback] Current State: %s%n", currentState.entrySet());

    if (Boolean.TRUE.equals(currentState.get("skip_llm_agent"))) {
      System.out.printf("[Callback] Skipping agent %s%n", agentName);
      return Maybe.just(
          Content.fromParts(Part.fromText(
              String.format("Agent %s skipped by before_agent_callback due to state.", agentName))));
    }

    System.out.printf("[Callback] Proceeding with agent %s%n", agentName);
    return Maybe.empty();
  }

  public void defineAgent(String prompt) {
    BaseAgent llmAgentWithBeforeCallback =
        LlmAgent.builder()
            .model(MODEL_NAME)
            .name(APP_NAME)
            .instruction("You are a concise assistant.")
            .description("An LLM agent demonstrating stateful before_agent_callback")
            .beforeAgentCallback(this::checkIfAgentShouldRun)
            .build();

    InMemoryRunner runner = new InMemoryRunner(llmAgentWithBeforeCallback, APP_NAME);
    // Scenario 1: no skip flag
    runAgent(runner, null, prompt);
    // Scenario 2: skip flag set
    runAgent(runner, new ConcurrentHashMap<>(Map.of("skip_llm_agent", true)), prompt);
  }

  public void runAgent(InMemoryRunner runner, ConcurrentHashMap<String, Object> initialState, String prompt) {
    Session session =
        runner.sessionService().createSession(APP_NAME, USER_ID, initialState, SESSION_ID).blockingGet();
    Content userMessage = Content.fromParts(Part.fromText(prompt));
    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    eventStream.blockingForEach(event -> {
      if (event.finalResponse()) {
        System.out.println(event.stringifyContent());
      }
    });
  }
}
```

## after_agent_callback

Checks `add_concluding_note` in session state. Returns `Maybe.just(Content)` to replace the agent's output, or `Maybe.empty()` to pass through the original.

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.CallbackContext;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.State;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class AfterAgentCallbackExample {

  private static final String APP_NAME = "after_agent_demo";
  private static final String USER_ID = "test_user_after";
  private static final String SESSION_ID_NORMAL = "session_run_normally";
  private static final String SESSION_ID_MODIFY = "session_modify_output";
  private static final String MODEL_NAME = "gemini-2.0-flash";

  public static void main(String[] args) {
    AfterAgentCallbackExample demo = new AfterAgentCallbackExample();
    demo.defineAgentAndRunScenarios();
  }

  // Checks 'add_concluding_note' in state. Returns replacement Content or Maybe.empty().
  public Maybe<Content> modifyOutputAfterAgent(CallbackContext callbackContext) {
    String agentName = callbackContext.agentName();
    State currentState = callbackContext.state();

    System.out.printf("%n[Callback] Exiting agent: %s%n", agentName);
    System.out.printf("[Callback] Current State: %s%n", currentState.entrySet());

    if (Boolean.TRUE.equals(currentState.get("add_concluding_note"))) {
      System.out.printf("[Callback] Replacing agent %s's output.%n", agentName);
      return Maybe.just(
          Content.builder()
              .parts(List.of(Part.fromText(
                  "Concluding note added by after_agent_callback, replacing original output.")))
              .role("model")
              .build());
    } else {
      System.out.printf("[Callback] Using agent %s's original output.%n", agentName);
      return Maybe.empty();
    }
  }

  public void defineAgentAndRunScenarios() {
    LlmAgent llmAgentWithAfterCb =
        LlmAgent.builder()
            .name(APP_NAME)
            .model(MODEL_NAME)
            .description("An LLM agent demonstrating after_agent_callback for output modification")
            .instruction("You are a simple agent. Just say 'Processing complete!'")
            .afterAgentCallback(this::modifyOutputAfterAgent)
            .build();

    InMemoryRunner runner = new InMemoryRunner(llmAgentWithAfterCb, APP_NAME);

    // Scenario 1: original output is used
    runScenario(runner, llmAgentWithAfterCb.name(), SESSION_ID_NORMAL, null, "Process this please.");

    // Scenario 2: callback replaces the agent's output
    Map<String, Object> modifyState = new HashMap<>();
    modifyState.put("add_concluding_note", true);
    runScenario(runner, llmAgentWithAfterCb.name(), SESSION_ID_MODIFY,
        new ConcurrentHashMap<>(modifyState), "Process this and add note.");
  }

  public void runScenario(
      InMemoryRunner runner, String appName, String sessionId,
      ConcurrentHashMap<String, Object> initialState, String userQuery) {
    runner.sessionService().createSession(appName, USER_ID, initialState, sessionId).blockingGet();
    Content userMessage = Content.builder().role("user").parts(List.of(Part.fromText(userQuery))).build();
    Flowable<Event> eventStream = runner.runAsync(USER_ID, sessionId, userMessage);
    eventStream.blockingForEach(event -> {
      if (event.finalResponse() && event.content().isPresent()) {
        System.out.printf("Final Output for %s: %s%n", sessionId, event.stringifyContent());
      }
    });
  }
}
```

## before_model_callback

Modifies `LlmRequest` system instruction (adds a prefix) and returns `Maybe.just(LlmResponse)` to block the LLM call when "BLOCK" appears in the user message, or `Maybe.empty()` to proceed.

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.CallbackContext;
import com.google.adk.events.Event;
import com.google.adk.models.LlmRequest;
import com.google.adk.models.LlmResponse;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.Iterables;
import com.google.genai.types.Content;
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;
import java.util.ArrayList;
import java.util.List;

public class BeforeModelCallbackExample {

  private static final String AGENT_NAME = "ModelCallbackAgent";
  private static final String MODEL_NAME = "gemini-2.0-flash";
  private static final String APP_NAME = "guardrail_app_java";
  private static final String USER_ID = "user_1_java";

  public static void main(String[] args) {
    BeforeModelCallbackExample demo = new BeforeModelCallbackExample();
    demo.defineAgentAndRun();
  }

  // Modifies system instruction and optionally skips the LLM call.
  public Maybe<LlmResponse> simpleBeforeModelModifier(
      CallbackContext callbackContext, LlmRequest llmRequest) {
    String agentName = callbackContext.agentName();
    System.out.printf("%n[Callback] Before model call for agent: %s%n", agentName);

    String lastUserMessage = "";
    if (llmRequest.contents() != null && !llmRequest.contents().isEmpty()) {
      Content lastContentItem = Iterables.getLast(llmRequest.contents());
      if ("user".equals(lastContentItem.role().orElse(null))
          && lastContentItem.parts().isPresent()
          && !lastContentItem.parts().get().isEmpty()) {
        lastUserMessage = lastContentItem.parts().get().get(0).text().orElse("");
      }
    }
    System.out.printf("[Callback] Last user message: '%s'%n", lastUserMessage);

    // Modification: prefix the system instruction
    Content systemInstruction = Content.builder().parts(ImmutableList.of()).build();
    if (llmRequest.config().isPresent()) {
      systemInstruction = llmRequest.config().get().systemInstruction()
          .orElseGet(() -> Content.builder().role("system").parts(ImmutableList.of()).build());
    }
    List<Part> currentParts = new ArrayList<>(systemInstruction.parts().orElse(ImmutableList.of()));
    if (currentParts.isEmpty()) currentParts.add(Part.fromText(""));
    String prefix = "[Modified by Callback] ";
    String modifiedText = prefix + currentParts.get(0).text().orElse("");
    llmRequest = llmRequest.toBuilder()
        .config(GenerateContentConfig.builder()
            .systemInstruction(Content.builder()
                .parts(List.of(Part.fromText(modifiedText))).build())
            .build())
        .build();
    System.out.printf("[Callback] Modified system instruction to: '%s'%n", modifiedText);

    // Skip: block if user message contains "BLOCK"
    if (lastUserMessage.toUpperCase().contains("BLOCK")) {
      System.out.println("[Callback] 'BLOCK' keyword found. Skipping LLM call.");
      return Maybe.just(
          LlmResponse.builder()
              .content(Content.builder()
                  .role("model")
                  .parts(ImmutableList.of(Part.fromText("LLM call was blocked by before_model_callback.")))
                  .build())
              .build());
    }

    System.out.println("[Callback] Proceeding with LLM call.");
    return Maybe.empty();
  }

  public void defineAgentAndRun() {
    LlmAgent myLlmAgent = LlmAgent.builder()
        .name(AGENT_NAME)
        .model(MODEL_NAME)
        .instruction("You are a helpful assistant.")
        .description("An LLM agent demonstrating before_model_callback")
        .beforeModelCallback(this::simpleBeforeModelModifier)
        .build();

    InMemoryRunner runner = new InMemoryRunner(myLlmAgent, APP_NAME);
    Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
    Content userMessage = Content.fromParts(Part.fromText("Tell me about quantum computing. BLOCK."));

    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    eventStream.blockingForEach(event -> {
      if (event.finalResponse()) {
        System.out.println(event.stringifyContent());
      }
    });
  }
}
```

## after_model_callback

Inspects the LLM response and replaces "joke" with "funny story". Returns `Maybe.just(LlmResponse)` on modification, or `Maybe.empty()` to pass through unchanged.

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.CallbackContext;
import com.google.adk.events.Event;
import com.google.adk.models.LlmResponse;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.common.collect.ImmutableList;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class AfterModelCallbackExample {

  private static final String AGENT_NAME = "AfterModelCallbackAgent";
  private static final String MODEL_NAME = "gemini-2.0-flash";
  private static final String APP_NAME = "AfterModelCallbackAgentApp";
  private static final String USER_ID = "user_1";
  private static final String SEARCH_TERM = "joke";
  private static final String REPLACE_TERM = "funny story";
  private static final Pattern SEARCH_PATTERN =
      Pattern.compile("\\b" + Pattern.quote(SEARCH_TERM) + "\\b", Pattern.CASE_INSENSITIVE);

  public static void main(String[] args) {
    AfterModelCallbackExample example = new AfterModelCallbackExample();
    example.defineAgentAndRun();
  }

  // Replaces "joke" with "funny story" in the LLM response text.
  public Maybe<LlmResponse> simpleAfterModelModifier(
      CallbackContext callbackContext, LlmResponse llmResponse) {
    String agentName = callbackContext.agentName();
    System.out.printf("%n[Callback] After model call for agent: %s%n", agentName);

    if (llmResponse.errorMessage().isPresent()) {
      System.out.printf("[Callback] Response has error. No modification.%n");
      return Maybe.empty();
    }

    Optional<Part> firstTextPartOpt = llmResponse.content()
        .flatMap(Content::parts)
        .filter(parts -> !parts.isEmpty() && parts.get(0).text().isPresent())
        .map(parts -> parts.get(0));

    if (!firstTextPartOpt.isPresent()) {
      System.out.println("[Callback] No text content to modify.");
      return Maybe.empty();
    }

    String originalText = firstTextPartOpt.get().text().get();
    System.out.printf("[Callback] Inspected original text: '%.100s...'%n", originalText);

    Matcher matcher = SEARCH_PATTERN.matcher(originalText);
    if (!matcher.find()) {
      System.out.printf("[Callback] '%s' not found. Passing original response through.%n", SEARCH_TERM);
      return Maybe.empty();
    }

    System.out.printf("[Callback] Found '%s'. Modifying response.%n", SEARCH_TERM);
    String foundTerm = matcher.group(0);
    String actualReplaceTerm = Character.isUpperCase(foundTerm.charAt(0))
        ? Character.toUpperCase(REPLACE_TERM.charAt(0)) + REPLACE_TERM.substring(1)
        : REPLACE_TERM;
    String modifiedText = matcher.replaceFirst(Matcher.quoteReplacement(actualReplaceTerm));

    Content originalContent = llmResponse.content().get();
    List<Part> originalParts = originalContent.parts().orElse(ImmutableList.of());
    List<Part> modifiedParts = new ArrayList<>();
    modifiedParts.add(Part.fromText(modifiedText));
    for (int i = 1; i < originalParts.size(); i++) modifiedParts.add(originalParts.get(i));

    System.out.println("[Callback] Returning modified response.");
    return Maybe.just(
        LlmResponse.builder()
            .content(originalContent.toBuilder().parts(ImmutableList.copyOf(modifiedParts)).build())
            .groundingMetadata(llmResponse.groundingMetadata())
            .build());
  }

  public void defineAgentAndRun() {
    LlmAgent myLlmAgent = LlmAgent.builder()
        .name(AGENT_NAME)
        .model(MODEL_NAME)
        .instruction("You are a helpful assistant.")
        .description("An LLM agent demonstrating after_model_callback")
        .afterModelCallback(this::simpleAfterModelModifier)
        .build();

    InMemoryRunner runner = new InMemoryRunner(myLlmAgent, APP_NAME);
    Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
    Content userMessage = Content.fromParts(
        Part.fromText("Tell me a joke about quantum computing. Include the word 'joke' in your response."));

    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    eventStream.blockingForEach(event -> {
      if (event.finalResponse()) {
        System.out.println(event.stringifyContent());
      }
    });
  }
}
```

## before_tool_callback

Modifies tool `args` map (redirects "canada" to "France") or returns a result map to skip tool execution entirely when "BLOCK" is passed.

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.InvocationContext;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.Annotations.Schema;
import com.google.adk.tools.BaseTool;
import com.google.adk.tools.FunctionTool;
import com.google.adk.tools.ToolContext;
import com.google.common.collect.ImmutableMap;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;
import java.util.HashMap;
import java.util.Map;

public class BeforeToolCallbackExample {

  private static final String APP_NAME = "ToolCallbackAgentApp";
  private static final String USER_ID = "user_1";
  private static final String SESSION_ID = "session_001";
  private static final String MODEL_NAME = "gemini-2.0-flash";

  public static void main(String[] args) {
    BeforeToolCallbackExample example = new BeforeToolCallbackExample();
    example.runAgent("capital of canada");
  }

  // Tool: looks up the capital city.
  public static Map<String, Object> getCapitalCity(
      @Schema(name = "country", description = "The country to find the capital of.") String country) {
    System.out.printf("--- Tool 'getCapitalCity' executing with country: %s ---%n", country);
    Map<String, String> countryCapitals = new HashMap<>();
    countryCapitals.put("united states", "Washington, D.C.");
    countryCapitals.put("canada", "Ottawa");
    countryCapitals.put("france", "Paris");
    countryCapitals.put("germany", "Berlin");
    String capital = countryCapitals.getOrDefault(country.toLowerCase(), "Capital not found for " + country);
    return ImmutableMap.of("capital", capital);
  }

  // Modifies args or skips tool execution based on country value.
  public Maybe<Map<String, Object>> simpleBeforeToolModifier(
      InvocationContext invocationContext, BaseTool tool,
      Map<String, Object> args, ToolContext toolContext) {
    String toolName = tool.name();
    System.out.printf("[Callback] Before tool call for tool '%s' in agent '%s'%n",
        toolName, invocationContext.agent().name());
    System.out.printf("[Callback] Original args: %s%n", args);

    if ("getCapitalCity".equals(toolName)) {
      String countryArg = (String) args.get("country");
      if (countryArg != null) {
        if ("canada".equalsIgnoreCase(countryArg)) {
          System.out.println("[Callback] Detected 'Canada'. Modifying args to 'France'.");
          args.put("country", "France");
          return Maybe.empty(); // proceed with modified args
        } else if ("BLOCK".equalsIgnoreCase(countryArg)) {
          System.out.println("[Callback] Detected 'BLOCK'. Skipping tool execution.");
          return Maybe.just(ImmutableMap.of("result", "Tool execution was blocked by before_tool_callback."));
        }
      }
    }

    System.out.println("[Callback] Proceeding with original or previously modified args.");
    return Maybe.empty();
  }

  public void runAgent(String query) {
    FunctionTool capitalTool = FunctionTool.create(this.getClass(), "getCapitalCity");

    LlmAgent myLlmAgent = LlmAgent.builder()
        .name(APP_NAME)
        .model(MODEL_NAME)
        .instruction("You are an agent that can find capital cities. Use the getCapitalCity tool.")
        .description("An LLM agent demonstrating before_tool_callback")
        .tools(capitalTool)
        .beforeToolCallback(this::simpleBeforeToolModifier)
        .build();

    InMemoryRunner runner = new InMemoryRunner(myLlmAgent);
    Session session = runner.sessionService().createSession(APP_NAME, USER_ID, null, SESSION_ID).blockingGet();
    Content userMessage = Content.fromParts(Part.fromText(query));

    System.out.printf("%n--- Calling agent with query: \"%s\" ---%n", query);
    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    eventStream.blockingForEach(event -> {
      if (event.finalResponse()) System.out.println(event.stringifyContent());
    });
  }
}
```

## after_tool_callback

Inspects the tool result map and appends a note when the capital is "Washington, D.C.". Returns `Maybe.just(modifiedMap)` or `Maybe.empty()` to pass through the original.

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.InvocationContext;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.Annotations.Schema;
import com.google.adk.tools.BaseTool;
import com.google.adk.tools.FunctionTool;
import com.google.adk.tools.ToolContext;
import com.google.common.collect.ImmutableMap;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import io.reactivex.rxjava3.core.Maybe;
import java.util.HashMap;
import java.util.Map;

public class AfterToolCallbackExample {

  private static final String APP_NAME = "AfterToolCallbackAgentApp";
  private static final String USER_ID = "user_1";
  private static final String SESSION_ID = "session_001";
  private static final String MODEL_NAME = "gemini-2.0-flash";

  public static void main(String[] args) {
    AfterToolCallbackExample example = new AfterToolCallbackExample();
    example.runAgent("What is the capital of the United States?");
  }

  // Tool: looks up the capital city.
  @Schema(description = "Retrieves the capital city of a given country.")
  public static Map<String, Object> getCapitalCity(
      @Schema(description = "The country to find the capital of.") String country) {
    System.out.printf("--- Tool 'getCapitalCity' executing with country: %s ---%n", country);
    Map<String, String> countryCapitals = new HashMap<>();
    countryCapitals.put("united states", "Washington, D.C.");
    countryCapitals.put("canada", "Ottawa");
    countryCapitals.put("france", "Paris");
    countryCapitals.put("germany", "Berlin");
    String capital = countryCapitals.getOrDefault(country.toLowerCase(), "Capital not found for " + country);
    return ImmutableMap.of("result", capital);
  }

  // Inspects tool result and appends a note when result is "Washington, D.C.".
  public Maybe<Map<String, Object>> simpleAfterToolModifier(
      InvocationContext invocationContext, BaseTool tool,
      Map<String, Object> args, ToolContext toolContext, Object toolResponse) {
    String toolName = tool.name();
    System.out.printf("[Callback] After tool call for tool '%s' in agent '%s'%n",
        toolName, invocationContext.agent().name());
    System.out.printf("[Callback] Args used: %s%n", args);
    System.out.printf("[Callback] Original tool_response: %s%n", toolResponse);

    if (!(toolResponse instanceof Map)) {
      System.out.println("[Callback] toolResponse is not a Map, cannot process further.");
      return Maybe.empty();
    }

    @SuppressWarnings("unchecked")
    Map<String, Object> responseMap = (Map<String, Object>) toolResponse;
    Object originalResultValue = responseMap.get("result");

    if ("getCapitalCity".equals(toolName) && "Washington, D.C.".equals(originalResultValue)) {
      System.out.println("[Callback] Detected 'Washington, D.C.'. Modifying tool response.");
      Map<String, Object> modifiedResponse = new HashMap<>(responseMap);
      modifiedResponse.put("result", originalResultValue + " (Note: This is the capital of the USA).");
      modifiedResponse.put("note_added_by_callback", true);
      System.out.printf("[Callback] Modified tool_response: %s%n", modifiedResponse);
      return Maybe.just(modifiedResponse);
    }

    System.out.println("[Callback] Passing original tool response through.");
    return Maybe.empty();
  }

  public void runAgent(String query) {
    FunctionTool capitalTool = FunctionTool.create(this.getClass(), "getCapitalCity");

    LlmAgent myLlmAgent = LlmAgent.builder()
        .name(APP_NAME)
        .model(MODEL_NAME)
        .instruction("You are an agent that finds capital cities using the getCapitalCity tool. Report the result clearly.")
        .description("An LLM agent demonstrating after_tool_callback")
        .tools(capitalTool)
        .afterToolCallback(this::simpleAfterToolModifier)
        .build();

    InMemoryRunner runner = new InMemoryRunner(myLlmAgent);
    Session session = runner.sessionService().createSession(APP_NAME, USER_ID, null, SESSION_ID).blockingGet();
    Content userMessage = Content.fromParts(Part.fromText(query));

    System.out.printf("%n--- Calling agent with query: \"%s\" ---%n", query);
    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    eventStream.blockingForEach(event -> {
      if (event.finalResponse()) System.out.println(event.stringifyContent());
    });
  }
}
```
