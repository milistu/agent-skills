# Multi-Agent Systems — Java Examples

## 1.1. Agent Hierarchy (Parent agent, Sub Agents)

Defines a parent `LlmAgent` with two child agents passed via `.subAgents()`; the framework automatically sets `parentAgent()` on each child.

```java
// Conceptual Example: Defining Hierarchy
import com.google.adk.agents.SequentialAgent;
import com.google.adk.agents.LlmAgent;

// Define individual agents
LlmAgent greeter = LlmAgent.builder().name("Greeter").model("gemini-2.0-flash").build();
SequentialAgent taskDoer = SequentialAgent.builder().name("TaskExecutor").subAgents(...).build(); // Sequential Agent

// Create parent agent and assign sub_agents
LlmAgent coordinator = LlmAgent.builder()
    .name("Coordinator")
    .model("gemini-2.0-flash")
    .description("I coordinate greetings and tasks")
    .subAgents(greeter, taskDoer) // Assign subAgents here
    .build();

// Framework automatically sets:
// assert greeter.parentAgent().equals(coordinator);
// assert taskDoer.parentAgent().equals(coordinator);
```

## 1.2. Workflow Agents as Orchestrators

### SequentialAgent — outputKey pipeline chaining

Passes `.outputKey("data")` on the first agent so its response is stored in `state.get("data")`, which the second agent reads via instruction template substitution.

```java
// Conceptual Example: Sequential Pipeline
import com.google.adk.agents.SequentialAgent;
import com.google.adk.agents.LlmAgent;

LlmAgent step1 = LlmAgent.builder().name("Step1_Fetch").outputKey("data").build(); // Saves output to state.get("data")
LlmAgent step2 = LlmAgent.builder().name("Step2_Process").instruction("Process data from {data}.").build();

SequentialAgent pipeline = SequentialAgent.builder().name("MyPipeline").subAgents(step1, step2).build();
// When pipeline runs, Step2 can access the state.get("data") set by Step1.
```

### ParallelAgent — shared session state with distinct output keys

Two sub-agents run concurrently and write to separate state keys; a downstream agent reads both after the parallel phase completes.

```java
// Conceptual Example: Parallel Execution
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.ParallelAgent;

LlmAgent fetchWeather = LlmAgent.builder()
    .name("WeatherFetcher")
    .outputKey("weather")
    .build();

LlmAgent fetchNews = LlmAgent.builder()
    .name("NewsFetcher")
    .instruction("news")
    .build();

ParallelAgent gatherer = ParallelAgent.builder()
    .name("InfoGatherer")
    .subAgents(fetchWeather, fetchNews)
    .build();

// When gatherer runs, WeatherFetcher and NewsFetcher run concurrently.
// A subsequent agent could read state['weather'] and state['news'].
```

### LoopAgent — custom BaseAgent escalates when condition is met

A custom `BaseAgent` subclass checks `session.state` each iteration and sets `.escalate(isDone)` in `EventActions` to break the loop.

```java
// Conceptual Example: Loop with Condition
// Custom agent to check state and potentially escalate
public static class CheckConditionAgent extends BaseAgent {
  public CheckConditionAgent(String name, String description) {
    super(name, description, List.of(), null, null);
  }

  @Override
  protected Flowable<Event> runAsyncImpl(InvocationContext ctx) {
    String status = (String) ctx.session().state().getOrDefault("status", "pending");
    boolean isDone = "completed".equalsIgnoreCase(status);

    // Emit an event that signals to escalate (exit the loop) if the condition is met.
    Event checkEvent = Event.builder()
            .author(name())
            .id(Event.generateEventId())
            .actions(EventActions.builder().escalate(isDone).build()) // Escalate if done
            .build();
    return Flowable.just(checkEvent);
  }
}

// Agent that might update state.put("status")
LlmAgent processingStepAgent = LlmAgent.builder().name("ProcessingStep").build();
CheckConditionAgent conditionCheckerAgent = new CheckConditionAgent(
    "ConditionChecker",
    "Checks if the status is 'completed'."
);
LoopAgent poller = LoopAgent.builder().name("StatusPoller").maxIterations(10).subAgents(processingStepAgent, conditionCheckerAgent).build();
// Executes processingStepAgent then conditionCheckerAgent repeatedly until escalate or 10 iterations.
```

## 1.3. Interaction & Communication Mechanisms

### Shared Session State — outputKey chaining

`agentA` saves its response to `state("capital_city")` via `.outputKey()`; `agentB`'s instruction template reads it automatically.

```java
// Conceptual Example: Using outputKey and reading state
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.SequentialAgent;

LlmAgent agentA = LlmAgent.builder()
    .name("AgentA")
    .instruction("Find the capital of France.")
    .outputKey("capital_city")
    .build();

LlmAgent agentB = LlmAgent.builder()
    .name("AgentB")
    .instruction("Tell me about the city stored in {capital_city}.")
    .outputKey("capital_city")
    .build();

SequentialAgent pipeline = SequentialAgent.builder().name("CityInfo").subAgents(agentA, agentB).build();
// AgentA saves "Paris" to state('capital_city'); AgentB reads it.
```

### LLM-Driven Delegation — transfer_to_agent routing

The coordinator's LLM emits a `transferToAgent` function call; `AutoFlow` intercepts and routes execution to the named sub-agent.

```java
// Conceptual Setup: LLM Transfer
import com.google.adk.agents.LlmAgent;

LlmAgent bookingAgent = LlmAgent.builder()
    .name("Booker")
    .description("Handles flight and hotel bookings.")
    .build();

LlmAgent infoAgent = LlmAgent.builder()
    .name("Info")
    .description("Provides general information and answers questions.")
    .build();

// Define the coordinator agent
LlmAgent coordinator = LlmAgent.builder()
    .name("Coordinator")
    .model("gemini-2.0-flash")
    .instruction("You are an assistant. Delegate booking tasks to Booker and info requests to Info.")
    .description("Main coordinator.")
    // AutoFlow is used by default when subAgents are present and transfer is not disallowed.
    .subAgents(bookingAgent, infoAgent)
    .build();

// "Book a flight" -> transferToAgent(agentName='Booker')
// ADK framework routes execution to bookingAgent.
```

### AgentTool — wrapping an agent as a callable tool

`AgentTool.create()` wraps a custom `BaseAgent` so the parent LLM can invoke it like a regular tool; the tool captures the sub-agent's final response and returns it as the tool result.

```java
// Conceptual Setup: Agent as a Tool
import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.tools.AgentTool;

// Example custom agent
public class ImageGeneratorAgent extends BaseAgent {

  public ImageGeneratorAgent(String name, String description) {
    super(name, description, List.of(), null, null);
  }

  @Override
  protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
    invocationContext.session().state().get("image_prompt");
    // Generate image bytes ...
    Event responseEvent = Event.builder()
        .author(this.name())
        .content(Content.fromParts(Part.fromText("...")))
        .build();
    return Flowable.just(responseEvent);
  }

  @Override
  protected Flowable<Event> runLiveImpl(InvocationContext invocationContext) {
    return null;
  }
}

// Wrap the agent using AgentTool
ImageGeneratorAgent imageAgent = new ImageGeneratorAgent("image_agent", "generates images");
AgentTool imageTool = AgentTool.create(imageAgent);

// Parent agent uses the AgentTool
LlmAgent artistAgent = LlmAgent.builder()
        .name("Artist")
        .model("gemini-2.0-flash")
        .instruction(
                "You are an artist. Create a detailed prompt for an image and then " +
                        "use the 'ImageGen' tool to generate the image."
        )
        .description("An agent that can create images using a generation tool.")
        .tools(imageTool)
        .build();

// Artist LLM calls ImageGen tool; framework runs ImageGeneratorAgent and returns result.
```

## 2. Common Multi-Agent Patterns

### Coordinator/Dispatcher Pattern

LLM transfer routes each user request to a specialist sub-agent by description matching; `disallowTransferToParent` and `disallowTransferToPeers` can restrict scope.

```java
// Conceptual Code: Coordinator using LLM Transfer
import com.google.adk.agents.LlmAgent;

LlmAgent billingAgent = LlmAgent.builder()
    .name("Billing")
    .description("Handles billing inquiries and payment issues.")
    .build();

LlmAgent supportAgent = LlmAgent.builder()
    .name("Support")
    .description("Handles technical support requests and login problems.")
    .build();

LlmAgent coordinator = LlmAgent.builder()
    .name("HelpDeskCoordinator")
    .model("gemini-2.0-flash")
    .instruction("Route user requests: Use Billing agent for payment issues, Support agent for technical problems.")
    .description("Main help desk router.")
    .subAgents(billingAgent, supportAgent)
    // Agent transfer is implicit with subAgents in AutoFlow, unless specified
    // using .disallowTransferToParent() or disallowTransferToPeers()
    .build();

// "My payment failed" -> transferToAgent(agentName='Billing')
// "I can't log in"   -> transferToAgent(agentName='Support')
```

### Sequential Pipeline Pattern

Three-stage pipeline chains `.outputKey()` values so each agent reads the previous agent's result from state.

```java
// Conceptual Code: Sequential Data Pipeline
import com.google.adk.agents.SequentialAgent;

LlmAgent validator = LlmAgent.builder()
    .name("ValidateInput")
    .instruction("Validate the input")
    .outputKey("validation_status") // Saves to session.state["validation_status"]
    .build();

LlmAgent processor = LlmAgent.builder()
    .name("ProcessData")
    .instruction("Process data if {validation_status} is 'valid'")
    .outputKey("result") // Saves to session.state["result"]
    .build();

LlmAgent reporter = LlmAgent.builder()
    .name("ReportResult")
    .instruction("Report the result from {result}")
    .build();

SequentialAgent dataPipeline = SequentialAgent.builder()
    .name("DataPipeline")
    .subAgents(validator, processor, reporter)
    .build();

// validator -> state['validation_status'] -> processor -> state['result'] -> reporter
```

### Parallel Fan-Out/Gather Pattern

`ParallelAgent` fans out to two fetchers simultaneously; a downstream synthesizer inside a `SequentialAgent` gathers both state keys.

```java
// Conceptual Code: Parallel Information Gathering
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.ParallelAgent;
import com.google.adk.agents.SequentialAgent;

LlmAgent fetchApi1 = LlmAgent.builder()
    .name("API1Fetcher")
    .instruction("Fetch data from API 1.")
    .outputKey("api1_data")
    .build();

LlmAgent fetchApi2 = LlmAgent.builder()
    .name("API2Fetcher")
    .instruction("Fetch data from API 2.")
    .outputKey("api2_data")
    .build();

ParallelAgent gatherConcurrently = ParallelAgent.builder()
    .name("ConcurrentFetcher")
    .subAgents(fetchApi2, fetchApi1)
    .build();

LlmAgent synthesizer = LlmAgent.builder()
    .name("Synthesizer")
    .instruction("Combine results from {api1_data} and {api2_data}.")
    .build();

SequentialAgent overallWorkflow = SequentialAgent.builder()
    .name("FetchAndSynthesize")
    .subAgents(gatherConcurrently, synthesizer)
    .build();

// Fetchers run concurrently; synthesizer reads both state keys afterwards.
```

### Hierarchical Task Decomposition

A high-level `reportWriter` wraps a mid-level `researchAssistant` via `AgentTool.create()`, which itself wraps `webSearcher` and `summarizer` — three-level hierarchy.

```java
// Conceptual Code: Hierarchical Research Task
import com.google.adk.agents.LlmAgent;
import com.google.adk.tools.AgentTool;

// Low-level tool-like agents
LlmAgent webSearcher = LlmAgent.builder()
    .name("WebSearch")
    .description("Performs web searches for facts.")
    .build();

LlmAgent summarizer = LlmAgent.builder()
    .name("Summarizer")
    .description("Summarizes text.")
    .build();

// Mid-level agent combining tools
LlmAgent researchAssistant = LlmAgent.builder()
    .name("ResearchAssistant")
    .model("gemini-2.0-flash")
    .description("Finds and summarizes information on a topic.")
    .tools(AgentTool.create(webSearcher), AgentTool.create(summarizer))
    .build();

// High-level agent delegating research
LlmAgent reportWriter = LlmAgent.builder()
    .name("ReportWriter")
    .model("gemini-2.0-flash")
    .instruction("Write a report on topic X. Use the ResearchAssistant to gather information.")
    .tools(AgentTool.create(researchAssistant))
    .build();

// ReportWriter -> ResearchAssistant -> WebSearch / Summarizer; results flow back up.
```

### Review/Critique Pattern (Generator-Critic)

`DraftWriter` saves its output to `state['draft_text']` via `.outputKey()`; `FactChecker` reads that key and saves its verdict to `state['review_status']`.

```java
// Conceptual Code: Generator-Critic
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.SequentialAgent;

LlmAgent generator = LlmAgent.builder()
    .name("DraftWriter")
    .instruction("Write a short paragraph about subject X.")
    .outputKey("draft_text")
    .build();

LlmAgent reviewer = LlmAgent.builder()
    .name("FactChecker")
    .instruction("Review the text in {draft_text} for factual accuracy. Output 'valid' or 'invalid' with reasons.")
    .outputKey("review_status")
    .build();

// Optional: Further steps based on review_status

SequentialAgent reviewPipeline = SequentialAgent.builder()
    .name("WriteAndReview")
    .subAgents(generator, reviewer)
    .build();

// generator -> state['draft_text'] -> reviewer -> state['review_status']
```

### Iterative Refinement Pattern

`LoopAgent` cycles through a refiner, quality checker, and anonymous `BaseAgent` escalator; `escalate(shouldStop)` breaks the loop when `state.get("quality_status").equals("pass")`.

```java
// Conceptual Code: Iterative Code Refinement
import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.LoopAgent;
import com.google.adk.events.Event;
import com.google.adk.events.EventActions;
import com.google.adk.agents.InvocationContext;
import io.reactivex.rxjava3.core.Flowable;
import java.util.List;

// Agent to generate/refine code
LlmAgent codeRefiner = LlmAgent.builder()
    .name("CodeRefiner")
    .instruction("Read state['current_code'] (if exists) and state['requirements']. Generate/refine Java code.")
    .outputKey("current_code") // Overwrites previous code in state
    .build();

// Agent to check quality
LlmAgent qualityChecker = LlmAgent.builder()
    .name("QualityChecker")
    .instruction("Evaluate the code in state['current_code'] against state['requirements']. Output 'pass' or 'fail'.")
    .outputKey("quality_status")
    .build();

// Custom agent that escalates when quality_status == "pass"
BaseAgent checkStatusAndEscalate = new BaseAgent(
    "StopChecker", "Checks quality_status and escalates if 'pass'.", List.of(), null, null) {

  @Override
  protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
    String status = (String) invocationContext.session().state().getOrDefault("quality_status", "fail");
    boolean shouldStop = "pass".equals(status);

    EventActions actions = EventActions.builder().escalate(shouldStop).build();
    Event event = Event.builder()
        .author(this.name())
        .actions(actions)
        .build();
    return Flowable.just(event);
  }
};

LoopAgent refinementLoop = LoopAgent.builder()
    .name("CodeRefinementLoop")
    .maxIterations(5)
    .subAgents(codeRefiner, qualityChecker, checkStatusAndEscalate)
    .build();

// Refiner -> Checker -> StopChecker each iteration; stops on 'pass' or 5 iterations.
```

### Human-in-the-Loop Pattern

A `FunctionTool` wrapping an external approval method is given to `requestApproval`; it blocks until a human responds, then returns the decision into the sequential pipeline.

```java
// Conceptual Code: Using a Tool for Human Approval
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.SequentialAgent;
import com.google.adk.tools.FunctionTool;

// --- Assume external_approval_tool exists ---
// public boolean externalApprovalTool(float amount, String reason) { ... }
FunctionTool approvalTool = FunctionTool.create(externalApprovalTool);

// Agent that prepares the request
LlmAgent prepareRequest = LlmAgent.builder()
    .name("PrepareApproval")
    .instruction("Prepare the approval request details based on user input. Store amount and reason in state.")
    .build();

// Agent that calls the human approval tool
LlmAgent requestApproval = LlmAgent.builder()
    .name("RequestHumanApproval")
    .instruction("Use the external_approval_tool with amount from state['approval_amount'] and reason from state['approval_reason'].")
    .tools(approvalTool)
    .outputKey("human_decision")
    .build();

// Agent that proceeds based on human decision
LlmAgent processDecision = LlmAgent.builder()
    .name("ProcessDecision")
    .instruction("Check {human_decision}. If 'approved', proceed. If 'rejected', inform user.")
    .build();

SequentialAgent approvalWorkflow = SequentialAgent.builder()
    .name("HumanApprovalWorkflow")
    .subAgents(prepareRequest, requestApproval, processDecision)
    .build();
```
