# LLM Agent — Java Examples

## Instructions with State Templating

Demonstrates passing a text block instruction to `LlmAgent.builder()` with `{var}` template placeholders.

```java
LlmAgent capitalAgent =
    LlmAgent.builder()
        .model("gemini-2.5-flash")
        .name("capital_agent")
        .description("Answers user questions about the capital city of a given country.")
        .instruction(
            """
            You are an agent that provides the capital city of a country.
            When a user asks for the capital of a country:
            1. Identify the country name from the user's query.
            2. Use the `get_capital_city` tool to find the capital.
            3. Respond clearly to the user, stating the capital city.
            Example Query: "What's the capital of {country}?"
            Example Response: "The capital of France is Paris."
            """)
        // tools will be added next
        .build();
```

## Equipping the Agent: Tools

Demonstrates defining a static method with `@Schema` annotations and wrapping it with `FunctionTool.create()`; Java requires explicit wrapping unlike Python.

```java
// Define a tool method with @Schema annotations on parameters
public static Map<String, Object> getCapitalCity(
        @Schema(name = "country", description = "The country to get capital for")
        String country) {
    Map<String, String> countryCapitals = new HashMap<>();
    countryCapitals.put("canada", "Ottawa");
    countryCapitals.put("france", "Paris");
    countryCapitals.put("japan", "Tokyo");

    String result = countryCapitals.getOrDefault(
            country.toLowerCase(), "Sorry, I couldn't find the capital for " + country + ".");
    return Map.of("result", result); // Tools must return a Map
}

// Wrap the method as a FunctionTool
FunctionTool capitalTool = FunctionTool.create(experiment.getClass(), "getCapitalCity");

LlmAgent capitalAgent =
    LlmAgent.builder()
        .model("gemini-2.5-flash")
        .name("capital_agent")
        .description("Answers user questions about the capital city of a given country.")
        .instruction("You are an agent that provides the capital city of a country...")
        .tools(capitalTool)
        .build();
```

## Fine-Tuning LLM Generation (`generateContentConfig`)

Demonstrates configuring `temperature` and `maxOutputTokens` via `GenerateContentConfig`.

```java
import com.google.genai.types.GenerateContentConfig;

LlmAgent agent =
    LlmAgent.builder()
        // ... other params
        .generateContentConfig(GenerateContentConfig.builder()
            .temperature(0.2F) // More deterministic output
            .maxOutputTokens(250)
            .build())
        .build();
```

## Structured Output (`outputSchema` + `outputKey`)

Demonstrates using a `Schema` object as `outputSchema` to enforce JSON output and `outputKey` to store the result in session state. Tools cannot be used alongside `outputSchema`.

```java
import com.google.genai.types.Schema;
import java.util.Map;

private static final Schema CAPITAL_OUTPUT =
    Schema.builder()
        .type("OBJECT")
        .description("Schema for capital city information.")
        .properties(
            Map.of(
                "capital",
                Schema.builder()
                    .type("STRING")
                    .description("The capital city of the country.")
                    .build()))
        .build();

LlmAgent structuredCapitalAgent =
    LlmAgent.builder()
        // ... name, model, description
        .instruction(
            "You are a Capital Information Agent. Given a country, respond ONLY with a JSON object"
            + " containing the capital. Format: {\"capital\": \"capital_name\"}")
        .outputSchema(CAPITAL_OUTPUT)          // Enforce JSON output
        .outputKey("found_capital")            // Store result in state.get("found_capital")
        // Cannot use tools(getCapitalCity) effectively here
        .build();
```

## Code Execution

Full runnable example using `BuiltInCodeExecutionTool` to let the agent write and run Python code; demonstrates `Runner`, `InMemorySessionService`, and iterating `runAsync` events to detect `executableCode` and `codeExecutionResult` parts.

```java
import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.runner.Runner;
import com.google.adk.sessions.InMemorySessionService;
import com.google.adk.sessions.Session;
import com.google.adk.tools.BuiltInCodeExecutionTool;
import com.google.common.collect.ImmutableList;
import com.google.genai.types.Content;
import com.google.genai.types.Part;

public class CodeExecutionAgentApp {

  private static final String AGENT_NAME = "calculator_agent";
  private static final String APP_NAME = "calculator";
  private static final String USER_ID = "user1234";
  private static final String SESSION_ID = "session_code_exec_sync";
  private static final String GEMINI_MODEL = "gemini-2.0-flash";

  public static void callAgent(Runner runner, String query) {
    Content content =
        Content.builder().role("user").parts(ImmutableList.of(Part.fromText(query))).build();

    InMemorySessionService sessionService = (InMemorySessionService) runner.sessionService();
    Session session =
        sessionService
            .createSession(APP_NAME, USER_ID, /* state= */ null, SESSION_ID)
            .blockingGet();

    System.out.println("\n--- Running Query: " + query + " ---");
    final String[] finalResponseText = {"No final text response captured."};

    try {
      runner
          .runAsync(session.userId(), session.id(), content)
          .forEach(
              event -> {
                System.out.println("Event ID: " + event.id() + ", Author: " + event.author());

                boolean hasSpecificPart = false;
                if (event.content().isPresent() && event.content().get().parts().isPresent()) {
                  for (Part part : event.content().get().parts().get()) {
                    if (part.executableCode().isPresent()) {
                      System.out.println(
                          "  Debug: Agent generated code:\n```python\n"
                              + part.executableCode().get().code()
                              + "\n```");
                      hasSpecificPart = true;
                    } else if (part.codeExecutionResult().isPresent()) {
                      System.out.println(
                          "  Debug: Code Execution Result: "
                              + part.codeExecutionResult().get().outcome()
                              + " - Output:\n"
                              + part.codeExecutionResult().get().output());
                      hasSpecificPart = true;
                    } else if (part.text().isPresent() && !part.text().get().trim().isEmpty()) {
                      System.out.println("  Text: '" + part.text().get().trim() + "'");
                    }
                  }
                }

                if (!hasSpecificPart && event.finalResponse()) {
                  if (event.content().isPresent()
                      && event.content().get().parts().isPresent()
                      && !event.content().get().parts().get().isEmpty()
                      && event.content().get().parts().get().get(0).text().isPresent()) {
                    finalResponseText[0] =
                        event.content().get().parts().get().get(0).text().get().trim();
                    System.out.println("==> Final Agent Response: " + finalResponseText[0]);
                  } else {
                    System.out.println(
                        "==> Final Agent Response: [No text content in final event]");
                  }
                }
              });
    } catch (Exception e) {
      System.err.println("ERROR during agent run: " + e.getMessage());
      e.printStackTrace();
    }
    System.out.println("------------------------------");
  }

  public static void main(String[] args) {
    BuiltInCodeExecutionTool codeExecutionTool = new BuiltInCodeExecutionTool();

    BaseAgent codeAgent =
        LlmAgent.builder()
            .name(AGENT_NAME)
            .model(GEMINI_MODEL)
            .tools(ImmutableList.of(codeExecutionTool))
            .instruction(
                """
                You are a calculator agent.
                When given a mathematical expression, write and execute Python code to calculate the result.
                Return only the final numerical result as plain text, without markdown or code blocks.
                """)
            .description("Executes Python code to perform calculations.")
            .build();

    InMemorySessionService sessionService = new InMemorySessionService();
    Runner runner = new Runner(codeAgent, APP_NAME, null, sessionService);

    callAgent(runner, "Calculate the value of (5 + 7) * 3");
    callAgent(runner, "What is 10 factorial?");
  }
}
```

## Putting It Together: Full End-to-End Example

Full runnable example contrasting two agents: one uses a tool + `outputKey`, the other uses `outputSchema` + `outputKey` (no tools). Shows `FunctionTool.create()`, `inputSchema`, `Runner`, `InMemorySessionService`, `Flowable` event streaming, and reading back session state.

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.events.Event;
import com.google.adk.runner.Runner;
import com.google.adk.sessions.InMemorySessionService;
import com.google.adk.sessions.Session;
import com.google.adk.tools.Annotations;
import com.google.adk.tools.FunctionTool;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import com.google.genai.types.Schema;
import io.reactivex.rxjava3.core.Flowable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

public class LlmAgentExample {

  private static final String MODEL_NAME = "gemini-2.0-flash";
  private static final String APP_NAME = "capital_agent_tool";
  private static final String USER_ID = "test_user_456";
  private static final String SESSION_ID_TOOL_AGENT = "session_tool_agent_xyz";
  private static final String SESSION_ID_SCHEMA_AGENT = "session_schema_agent_xyz";

  // Input schema used by both agents
  private static final Schema COUNTRY_INPUT_SCHEMA =
      Schema.builder()
          .type("OBJECT")
          .description("Input for specifying a country.")
          .properties(
              Map.of(
                  "country",
                  Schema.builder()
                      .type("STRING")
                      .description("The country to get information about.")
                      .build()))
          .required(List.of("country"))
          .build();

  // Output schema ONLY for the second agent
  private static final Schema CAPITAL_INFO_OUTPUT_SCHEMA =
      Schema.builder()
          .type("OBJECT")
          .description("Schema for capital city information.")
          .properties(
              Map.of(
                  "capital",
                  Schema.builder()
                      .type("STRING")
                      .description("The capital city of the country.")
                      .build(),
                  "population_estimate",
                  Schema.builder()
                      .type("STRING")
                      .description("An estimated population of the capital city.")
                      .build()))
          .required(List.of("capital", "population_estimate"))
          .build();

  // Tool method — must return a Map; use @Annotations.Schema to document parameters
  public static Map<String, Object> getCapitalCity(
      @Annotations.Schema(name = "country", description = "The country to get capital for")
      String country) {
    System.out.printf("%n-- Tool Call: getCapitalCity(country='%s') --%n", country);
    Map<String, String> countryCapitals = new HashMap<>();
    countryCapitals.put("united states", "Washington, D.C.");
    countryCapitals.put("canada", "Ottawa");
    countryCapitals.put("france", "Paris");
    countryCapitals.put("japan", "Tokyo");

    String result = countryCapitals.getOrDefault(
        country.toLowerCase(), "Sorry, I couldn't find the capital for " + country + ".");
    System.out.printf("-- Tool Result: '%s' --%n", result);
    return Map.of("result", result);
  }

  public static void main(String[] args) {
    LlmAgentExample agentExample = new LlmAgentExample();
    FunctionTool capitalTool = FunctionTool.create(agentExample.getClass(), "getCapitalCity");

    // Agent 1: Uses a tool and outputKey
    LlmAgent capitalAgentWithTool =
        LlmAgent.builder()
            .model(MODEL_NAME)
            .name("capital_agent_tool")
            .description("Retrieves the capital city using a specific tool.")
            .instruction(
              """
              You are a helpful agent that provides the capital city of a country using a tool.
              1. Extract the country name.
              2. Use the `get_capital_city` tool to find the capital.
              3. Respond clearly to the user, stating the capital city found by the tool.
              """)
            .tools(capitalTool)
            .inputSchema(COUNTRY_INPUT_SCHEMA)
            .outputKey("capital_tool_result")
            .build();

    // Agent 2: Uses outputSchema (NO tools possible)
    LlmAgent structuredInfoAgentSchema =
        LlmAgent.builder()
            .model(MODEL_NAME)
            .name("structured_info_agent_schema")
            .description("Provides capital and estimated population in a specific JSON format.")
            .instruction(
                String.format("""
                You are an agent that provides country information.
                Respond ONLY with a JSON object matching this exact schema: %s
                Use your knowledge. Do not use any tools.
                """, CAPITAL_INFO_OUTPUT_SCHEMA.toJson()))
            // *** NO tools here - using outputSchema prevents tool use ***
            .inputSchema(COUNTRY_INPUT_SCHEMA)
            .outputSchema(CAPITAL_INFO_OUTPUT_SCHEMA)
            .outputKey("structured_info_result")
            .build();

    InMemorySessionService sessionService = new InMemorySessionService();
    sessionService.createSession(APP_NAME, USER_ID, null, SESSION_ID_TOOL_AGENT).blockingGet();
    sessionService.createSession(APP_NAME, USER_ID, null, SESSION_ID_SCHEMA_AGENT).blockingGet();

    Runner capitalRunner = new Runner(capitalAgentWithTool, APP_NAME, null, sessionService);
    Runner structuredRunner = new Runner(structuredInfoAgentSchema, APP_NAME, null, sessionService);

    System.out.println("--- Testing Agent with Tool ---");
    agentExample.callAgentAndPrint(capitalRunner, capitalAgentWithTool, SESSION_ID_TOOL_AGENT, "{\"country\": \"France\"}");
    agentExample.callAgentAndPrint(capitalRunner, capitalAgentWithTool, SESSION_ID_TOOL_AGENT, "{\"country\": \"Canada\"}");

    System.out.println("\n--- Testing Agent with Output Schema (No Tool Use) ---");
    agentExample.callAgentAndPrint(structuredRunner, structuredInfoAgentSchema, SESSION_ID_SCHEMA_AGENT, "{\"country\": \"France\"}");
    agentExample.callAgentAndPrint(structuredRunner, structuredInfoAgentSchema, SESSION_ID_SCHEMA_AGENT, "{\"country\": \"Japan\"}");
  }

  // Runs the agent, prints the final response, and reads back the stored output_key from state.
  public void callAgentAndPrint(Runner runner, LlmAgent agent, String sessionId, String queryJson) {
    System.out.printf(
        "%n>>> Calling Agent: '%s' | Session: '%s' | Query: %s%n",
        agent.name(), sessionId, queryJson);

    Content userContent = Content.fromParts(Part.fromText(queryJson));
    final String[] finalResponseContent = {"No final response received."};
    Flowable<Event> eventStream = runner.runAsync(USER_ID, sessionId, userContent);

    eventStream.blockingForEach(event -> {
      if (event.finalResponse() && event.content().isPresent()) {
        event.content().get()
            .parts()
            .flatMap(parts -> parts.isEmpty() ? Optional.empty() : Optional.of(parts.get(0)))
            .flatMap(Part::text)
            .ifPresent(text -> finalResponseContent[0] = text);
      }
    });

    System.out.printf("<<< Agent '%s' Response: %s%n", agent.name(), finalResponseContent[0]);

    Session updatedSession =
        runner.sessionService()
            .getSession(APP_NAME, USER_ID, sessionId, Optional.empty())
            .blockingGet();

    if (updatedSession != null && agent.outputKey().isPresent()) {
      System.out.printf("--- Session State ['%s']: %s%n",
          agent.outputKey().get(),
          updatedSession.state().get(agent.outputKey().get()));
    }
  }
}
```
