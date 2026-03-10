# Function Tools — Java Examples

## Function Tool Example — Stock Price Agent

Full working example: `getStockPrice` is annotated with `@Schema`, wrapped via `FunctionTool.create`, and registered on an `LlmAgent`. Uses `InMemoryRunner` and RxJava `Flowable`.

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.Annotations.Schema;
import com.google.adk.tools.FunctionTool;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import java.util.HashMap;
import java.util.Map;

public class StockPriceAgent {

  private static final String APP_NAME = "stock_agent";
  private static final String USER_ID = "user1234";

  // Mock stock price data — replace with a real API in production.
  private static final Map<String, Double> mockStockPrices = new HashMap<>();

  static {
    mockStockPrices.put("GOOG", 1.0);
    mockStockPrices.put("AAPL", 1.0);
    mockStockPrices.put("MSFT", 1.0);
  }

  // The @Schema annotation on the method and parameters drives schema generation for the LLM.
  @Schema(description = "Retrieves the current stock price for a given symbol.")
  public static Map<String, Object> getStockPrice(
      @Schema(description = "The stock symbol (e.g., \"AAPL\", \"GOOG\")", name = "symbol")
      String symbol) {
    try {
      if (mockStockPrices.containsKey(symbol.toUpperCase())) {
        double currentPrice = mockStockPrices.get(symbol.toUpperCase());
        System.out.println("Tool: Found price for " + symbol + ": " + currentPrice);
        return Map.of("symbol", symbol, "price", currentPrice);
      } else {
        return Map.of("symbol", symbol, "error", "No data found for symbol");
      }
    } catch (Exception e) {
      return Map.of("symbol", symbol, "error", e.getMessage());
    }
  }

  public static void callAgent(String prompt) {
    // Create the FunctionTool from the Java method via reflection
    FunctionTool getStockPriceTool = FunctionTool.create(StockPriceAgent.class, "getStockPrice");

    LlmAgent stockPriceAgent =
        LlmAgent.builder()
            .model("gemini-2.0-flash")
            .name("stock_agent")
            .instruction(
                "You are an agent who retrieves stock prices. If a ticker symbol is provided, fetch the current price. If only a company name is given, first perform a Google search to find the correct ticker symbol before retrieving the stock price. If the provided ticker symbol is invalid or data cannot be retrieved, inform the user that the stock price could not be found.")
            .description(
                "This agent specializes in retrieving real-time stock prices. Given a stock ticker symbol (e.g., AAPL, GOOG, MSFT) or the stock name, use the tools and reliable data sources to provide the most up-to-date price.")
            .tools(getStockPriceTool)
            .build();

    InMemoryRunner runner = new InMemoryRunner(stockPriceAgent, APP_NAME);
    Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
    Content userMessage = Content.fromParts(Part.fromText(prompt));

    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);

    eventStream.blockingForEach(
        event -> {
          if (event.finalResponse()) {
            System.out.println(event.stringifyContent());
          }
        });
  }

  public static void main(String[] args) {
    callAgent("stock price of GOOG");
    callAgent("What's the price of MSFT?");
    callAgent("Can you find the stock price for an unknown company XYZ?");
  }
}
```

## LongRunningFunctionTool — Creating the Tool

`askForApproval` is wrapped via `LongRunningFunctionTool.create` so the framework pauses agent execution and waits for a client-provided `FunctionResponse`.

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.tools.LongRunningFunctionTool;
import java.util.HashMap;
import java.util.Map;

public class ExampleLongRunningFunction {

  // Define your Long Running function.
  // Returns an initial "pending" result so the client can track progress.
  public static Map<String, Object> askForApproval(String purpose, double amount) {
    System.out.println(
        "Simulating ticket creation for purpose: " + purpose + ", amount: " + amount);
    Map<String, Object> result = new HashMap<>();
    result.put("status", "pending");
    result.put("approver", "Sean Zhou");
    result.put("purpose", purpose);
    result.put("amount", amount);
    result.put("ticket-id", "approval-ticket-1");
    return result;
  }

  public static void main(String[] args) throws NoSuchMethodException {
    // Pass the method name to LongRunningFunctionTool.create via reflection
    LongRunningFunctionTool approveTool =
        LongRunningFunctionTool.create(ExampleLongRunningFunction.class, "askForApproval");

    LlmAgent approverAgent =
        LlmAgent.builder()
            // ...
            .tools(approveTool)
            .build();
  }
}
```

## Java ADK: Maven Compiler Plugin for `ToolContext` Parameter Names

When passing `ToolContext` to a function tool, add `-parameters` to the Maven compiler plugin so ADK can read the parameter name at runtime (alternatively annotate with `@Schema(name = "toolContext")`).

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.14.0</version>
            <configuration>
                <compilerArgs>
                    <arg>-parameters</arg>
                </compilerArgs>
            </configuration>
        </plugin>
    </plugins>
</build>
```

## LongRunningFunctionTool — Intermediate / Final Result Updates (Complete Multi-Turn Example)

Full three-turn workflow: Turn 1 captures the function call ID; Turn 2 provides a `ticket_id`; Turn 3 delivers the final approved status. Uses `@Schema` on `ToolContext` for ADK injection.

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.runner.Runner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.Annotations.Schema;
import com.google.adk.tools.LongRunningFunctionTool;
import com.google.adk.tools.ToolContext;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableMap;
import com.google.genai.types.Content;
import com.google.genai.types.FunctionCall;
import com.google.genai.types.FunctionResponse;
import com.google.genai.types.Part;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicReference;
import java.util.stream.Collectors;

public class LongRunningFunctionExample {

  private static String USER_ID = "user123";

  // @Schema on the method provides the tool name and description for the LLM.
  // @Schema(name = "toolContext") on ToolContext ensures ADK injects it correctly.
  @Schema(
      name = "create_ticket_long_running",
      description = """
          Creates a new support ticket with a specified urgency level.
          Examples of urgency are 'high', 'medium', or 'low'.
          The ticket creation is a long-running process, and its ID will be provided when ready.
      """)
  public static void createTicketAsync(
      @Schema(
              name = "urgency",
              description =
                  "The urgency level for the new ticket, such as 'high', 'medium', or 'low'.")
          String urgency,
      @Schema(name = "toolContext") // Ensures ADK injection
          ToolContext toolContext) {
    System.out.printf(
        "TOOL_EXEC: 'create_ticket_long_running' called with urgency: %s (Call ID: %s)%n",
        urgency, toolContext.functionCallId().orElse("N/A"));
  }

  public static void main(String[] args) {
    LlmAgent agent =
        LlmAgent.builder()
            .name("ticket_agent")
            .description("Agent for creating tickets via a long-running task.")
            .model("gemini-2.0-flash")
            .tools(
                ImmutableList.of(
                    LongRunningFunctionTool.create(
                        LongRunningFunctionExample.class, "createTicketAsync")))
            .build();

    Runner runner = new InMemoryRunner(agent);
    Session session =
        runner.sessionService().createSession(agent.name(), USER_ID, null, null).blockingGet();

    // --- Turn 1: User requests ticket ---
    System.out.println("\n--- Turn 1: User Request ---");
    Content initialUserMessage =
        Content.fromParts(Part.fromText("Create a high urgency ticket for me."));

    // Capture the function call ID emitted during Turn 1
    AtomicReference<String> funcCallIdRef = new AtomicReference<>();
    runner
        .runAsync(USER_ID, session.id(), initialUserMessage)
        .blockingForEach(
            event -> {
              printEventSummary(event, "T1");
              if (funcCallIdRef.get() == null) {
                event.content().flatMap(Content::parts).orElse(ImmutableList.of()).stream()
                    .map(Part::functionCall)
                    .flatMap(Optional::stream)
                    .filter(fc -> "create_ticket_long_running".equals(fc.name().orElse("")))
                    .findFirst()
                    .flatMap(FunctionCall::id)
                    .ifPresent(funcCallIdRef::set);
              }
            });

    if (funcCallIdRef.get() == null) {
      System.out.println("ERROR: Tool 'create_ticket_long_running' not called in Turn 1.");
      return;
    }
    System.out.println("ACTION: Captured FunctionCall ID: " + funcCallIdRef.get());

    // --- Turn 2: App provides initial ticket_id ---
    System.out.println("\n--- Turn 2: App provides ticket_id ---");
    String ticketId = "TICKET-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    FunctionResponse ticketCreatedFuncResponse =
        FunctionResponse.builder()
            .name("create_ticket_long_running")
            .id(funcCallIdRef.get())
            .response(ImmutableMap.of("ticket_id", ticketId))
            .build();
    Content appResponseWithTicketId =
        Content.builder()
            .parts(ImmutableList.of(Part.builder().functionResponse(ticketCreatedFuncResponse).build()))
            .role("user")
            .build();

    runner
        .runAsync(USER_ID, session.id(), appResponseWithTicketId)
        .blockingForEach(event -> printEventSummary(event, "T2"));
    System.out.println("ACTION: Sent ticket_id " + ticketId + " to agent.");

    // --- Turn 3: App provides final ticket status ---
    System.out.println("\n--- Turn 3: App provides ticket status ---");
    FunctionResponse ticketStatusFuncResponse =
        FunctionResponse.builder()
            .name("create_ticket_long_running")
            .id(funcCallIdRef.get())
            .response(ImmutableMap.of("status", "approved", "ticket_id", ticketId))
            .build();
    Content appResponseWithStatus =
        Content.builder()
            .parts(ImmutableList.of(Part.builder().functionResponse(ticketStatusFuncResponse).build()))
            .role("user")
            .build();

    runner
        .runAsync(USER_ID, session.id(), appResponseWithStatus)
        .blockingForEach(event -> printEventSummary(event, "T3_FINAL"));
    System.out.println("Long running function completed successfully.");
  }

  private static void printEventSummary(Event event, String turnLabel) {
    event
        .content()
        .ifPresent(
            content -> {
              String text =
                  content.parts().orElse(ImmutableList.of()).stream()
                      .map(part -> part.text().orElse(""))
                      .filter(s -> !s.isEmpty())
                      .collect(Collectors.joining(" "));
              if (!text.isEmpty()) {
                System.out.printf("[%s][%s_TEXT]: %s%n", turnLabel, event.author(), text);
              }
              content.parts().orElse(ImmutableList.of()).stream()
                  .map(Part::functionCall)
                  .flatMap(Optional::stream)
                  .findFirst()
                  .ifPresent(
                      fc ->
                          System.out.printf(
                              "[%s][%s_CALL]: %s(%s) ID: %s%n",
                              turnLabel,
                              event.author(),
                              fc.name().orElse("N/A"),
                              fc.args().orElse(ImmutableMap.of()),
                              fc.id().orElse("N/A")));
            });
  }
}
```

## AgentTool — Usage

Minimal snippet: wrap an agent with `AgentTool.create` and add it to the parent agent.

```java
AgentTool.create(agent)
```

## AgentTool — Full Example with `skipSummarization`

A root agent delegates summarization to a `summaryAgent` via `AgentTool.create(summaryAgent, true)` (`true` = skip LLM re-summarization).

```java
import com.google.adk.agents.LlmAgent;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.AgentTool;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;

public class AgentToolCustomization {

  private static final String APP_NAME = "summary_agent";
  private static final String USER_ID = "user1234";

  public static void initAgentAndRun(String prompt) {

    LlmAgent summaryAgent =
        LlmAgent.builder()
            .model("gemini-2.0-flash")
            .name("summaryAgent")
            .instruction(
                "You are an expert summarizer. Please read the following text and provide a concise summary.")
            .description("Agent to summarize text")
            .build();

    // AgentTool.create(summaryAgent, true) sets skipSummarization = true
    LlmAgent rootAgent =
        LlmAgent.builder()
            .model("gemini-2.0-flash")
            .name("rootAgent")
            .instruction(
                "You are a helpful assistant. When the user provides a text, always use the 'summaryAgent' tool to generate a summary. Always forward the user's message exactly as received to the 'summaryAgent' tool, without modifying or summarizing it yourself. Present the response from the tool to the user.")
            .description("Assistant agent")
            .tools(AgentTool.create(summaryAgent, true))
            .build();

    InMemoryRunner runner = new InMemoryRunner(rootAgent, APP_NAME);
    Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
    Content userMessage = Content.fromParts(Part.fromText(prompt));

    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);

    eventStream.blockingForEach(
        event -> {
          if (event.finalResponse()) {
            System.out.println(event.stringifyContent());
          }
        });
  }

  public static void main(String[] args) {
    String longText =
        """
            Quantum computing represents a fundamentally different approach to computation,
            leveraging the bizarre principles of quantum mechanics to process information. Unlike classical computers
            that rely on bits representing either 0 or 1, quantum computers use qubits which can exist in a state of superposition - effectively
            being 0, 1, or a combination of both simultaneously. Furthermore, qubits can become entangled,
            meaning their fates are intertwined regardless of distance, allowing for complex correlations. This parallelism and
            interconnectedness grant quantum computers the potential to solve specific types of incredibly complex problems - such
            as drug discovery, materials science, complex system optimization, and breaking certain types of cryptography - far
            faster than even the most powerful classical supercomputers could ever achieve, although the technology is still largely in its developmental stages.""";

    initAgentAndRun(longText);
  }
}
```
