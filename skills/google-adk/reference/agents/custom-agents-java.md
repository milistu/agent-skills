# Custom Agents — Java Examples

## Design Pattern Example: `StoryFlowAgent`

### Part 1: Custom Agent Initialization

Defines `StoryFlowAgentExample` extending `BaseAgent`, storing sub-agent instances as final fields and passing them to `super(...)` as the top-level sub-agents list the framework tracks.

```java
private final LlmAgent storyGenerator;
private final LoopAgent loopAgent;
private final SequentialAgent sequentialAgent;

public StoryFlowAgentExample(
    String name, LlmAgent storyGenerator, LoopAgent loopAgent, SequentialAgent sequentialAgent) {
  super(
      name,
      "Orchestrates story generation, critique, revision, and checks.",
      List.of(storyGenerator, loopAgent, sequentialAgent),
      null,
      null);

  this.storyGenerator = storyGenerator;
  this.loopAgent = loopAgent;
  this.sequentialAgent = sequentialAgent;
}
```

### Part 2: Custom Execution Logic with State-Driven Conditional Regeneration

Implements `runAsyncImpl` using `Flowable.defer()` for lazy stage evaluation and `Flowable.concatArray()` for sequential chaining. Each deferred stage reads session state only after prior stages complete, enabling the conditional story regeneration on a `"negative"` tone result.

```java
@Override
protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
  logger.log(Level.INFO, () -> String.format("[%s] Starting story generation workflow.", name()));

  // Stage 1. Initial Story Generation
  Flowable<Event> storyGenFlow = runStage(storyGenerator, invocationContext, "StoryGenerator");

  // Stage 2: Critic-Reviser Loop (runs after story generation completes)
  Flowable<Event> criticReviserFlow = Flowable.defer(() -> {
    if (!isStoryGenerated(invocationContext)) {
      logger.log(Level.SEVERE,() ->
          String.format("[%s] Failed to generate initial story. Aborting after StoryGenerator.",
              name()));
      return Flowable.empty(); // Stop further processing if no story
    }
      logger.log(Level.INFO, () ->
          String.format("[%s] Story state after generator: %s",
              name(), invocationContext.session().state().get("current_story")));
      return runStage(loopAgent, invocationContext, "CriticReviserLoop");
  });

  // Stage 3: Post-Processing (runs after critic-reviser loop completes)
  Flowable<Event> postProcessingFlow = Flowable.defer(() -> {
    logger.log(Level.INFO, () ->
        String.format("[%s] Story state after loop: %s",
            name(), invocationContext.session().state().get("current_story")));
    return runStage(sequentialAgent, invocationContext, "PostProcessing");
  });

  // Stage 4: Conditional Regeneration (runs after post-processing completes)
  Flowable<Event> conditionalRegenFlow = Flowable.defer(() -> {
    String toneCheckResult = (String) invocationContext.session().state().get("tone_check_result");
    logger.log(Level.INFO, () -> String.format("[%s] Tone check result: %s", name(), toneCheckResult));

    if ("negative".equalsIgnoreCase(toneCheckResult)) {
      logger.log(Level.INFO, () ->
          String.format("[%s] Tone is negative. Regenerating story...", name()));
      return runStage(storyGenerator, invocationContext, "StoryGenerator (Regen)");
    } else {
      logger.log(Level.INFO, () ->
          String.format("[%s] Tone is not negative. Keeping current story.", name()));
      return Flowable.empty(); // No regeneration needed
    }
  });

  return Flowable.concatArray(storyGenFlow, criticReviserFlow, postProcessingFlow, conditionalRegenFlow)
      .doOnComplete(() -> logger.log(Level.INFO, () -> String.format("[%s] Workflow finished.", name())));
}

// Helper method for a single agent run stage with logging
private Flowable<Event> runStage(BaseAgent agentToRun, InvocationContext ctx, String stageName) {
  logger.log(Level.INFO, () -> String.format("[%s] Running %s...", name(), stageName));
  return agentToRun
      .runAsync(ctx)
      .doOnNext(event ->
          logger.log(Level.INFO,() ->
              String.format("[%s] Event from %s: %s", name(), stageName, event.toJson())))
      .doOnError(err ->
          logger.log(Level.SEVERE,
              String.format("[%s] Error in %s", name(), stageName), err))
      .doOnComplete(() ->
          logger.log(Level.INFO, () ->
              String.format("[%s] %s finished.", name(), stageName)));
}
```

### Part 3: LLM Sub-Agent and Workflow Agent Definitions

Defines each `LlmAgent` using the builder pattern with an `outputKey` so results are written into session state. The `LoopAgent` and `SequentialAgent` are also assembled here before being passed to the orchestrator constructor.

```java
// --- Define the individual LLM agents ---
LlmAgent storyGenerator =
    LlmAgent.builder()
        .name("StoryGenerator")
        .model(MODEL_NAME)
        .description("Generates the initial story.")
        .instruction(
            """
          You are a story writer. Write a short story (around 100 words) about a cat,
          based on the topic: {topic}
          """)
        .inputSchema(null)
        .outputKey("current_story") // Key for storing output in session state
        .build();

LlmAgent critic =
    LlmAgent.builder()
        .name("Critic")
        .model(MODEL_NAME)
        .description("Critiques the story.")
        .instruction(
            """
          You are a story critic. Review the story: {current_story}. Provide 1-2 sentences of constructive criticism
          on how to improve it. Focus on plot or character.
          """)
        .inputSchema(null)
        .outputKey("criticism") // Key for storing criticism in session state
        .build();

LlmAgent reviser =
    LlmAgent.builder()
        .name("Reviser")
        .model(MODEL_NAME)
        .description("Revises the story based on criticism.")
        .instruction(
            """
          You are a story reviser. Revise the story: {current_story}, based on the criticism: {criticism}. Output only the revised story.
          """)
        .inputSchema(null)
        .outputKey("current_story") // Overwrites the original story
        .build();

LlmAgent grammarCheck =
    LlmAgent.builder()
        .name("GrammarCheck")
        .model(MODEL_NAME)
        .description("Checks grammar and suggests corrections.")
        .instruction(
            """
           You are a grammar checker. Check the grammar of the story: {current_story}. Output only the suggested
           corrections as a list, or output 'Grammar is good!' if there are no errors.
           """)
        .outputKey("grammar_suggestions")
        .build();

LlmAgent toneCheck =
    LlmAgent.builder()
        .name("ToneCheck")
        .model(MODEL_NAME)
        .description("Analyzes the tone of the story.")
        .instruction(
            """
          You are a tone analyzer. Analyze the tone of the story: {current_story}. Output only one word: 'positive' if
          the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral'
          otherwise.
          """)
        .outputKey("tone_check_result") // This agent's output determines the conditional flow
        .build();

LoopAgent loopAgent =
    LoopAgent.builder()
        .name("CriticReviserLoop")
        .description("Iteratively critiques and revises the story.")
        .subAgents(critic, reviser)
        .maxIterations(2)
        .build();

SequentialAgent sequentialAgent =
    SequentialAgent.builder()
        .name("PostProcessing")
        .description("Performs grammar and tone checks sequentially.")
        .subAgents(grammarCheck, toneCheck)
        .build();
```

### Part 4: Instantiation and Running

Creates the `StoryFlowAgentExample`, sets up an `InMemoryRunner` and session with initial state (including the `topic` key), and runs the workflow blocking on the `Flowable` event stream.

```java
// --- Function to Interact with the Agent ---
// Sends a new topic to the agent (overwriting the initial one if needed)
// and runs the workflow.
public static void runAgent(StoryFlowAgentExample agent, String userTopic) {
  // --- Setup Runner and Session ---
  InMemoryRunner runner = new InMemoryRunner(agent);

  Map<String, Object> initialState = new HashMap<>();
  initialState.put("topic", "a brave kitten exploring a haunted house");

  Session session =
      runner
          .sessionService()
          .createSession(APP_NAME, USER_ID, new ConcurrentHashMap<>(initialState), SESSION_ID)
          .blockingGet();
  logger.log(Level.INFO, () -> String.format("Initial session state: %s", session.state()));

  session.state().put("topic", userTopic); // Update the state in the retrieved session
  logger.log(Level.INFO, () -> String.format("Updated session state topic to: %s", userTopic));

  Content userMessage = Content.fromParts(Part.fromText("Generate a story about: " + userTopic));
  // Use the modified session object for the run
  Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);

  final String[] finalResponse = {"No final response captured."};
  eventStream.blockingForEach(
      event -> {
        if (event.finalResponse() && event.content().isPresent()) {
          String author = event.author() != null ? event.author() : "UNKNOWN_AUTHOR";
          Optional<String> textOpt =
              event
                  .content()
                  .flatMap(Content::parts)
                  .filter(parts -> !parts.isEmpty())
                  .map(parts -> parts.get(0).text().orElse(""));

          logger.log(Level.INFO, () ->
              String.format("Potential final response from [%s]: %s", author, textOpt.orElse("N/A")));
          textOpt.ifPresent(text -> finalResponse[0] = text);
        }
      });

  System.out.println("\n--- Agent Interaction Result ---");
  System.out.println("Agent Final Response: " + finalResponse[0]);

  // Retrieve session again to see the final state after the run
  Session finalSession =
      runner
          .sessionService()
          .getSession(APP_NAME, USER_ID, SESSION_ID, Optional.empty())
          .blockingGet();

  assert finalSession != null;
  System.out.println("Final Session State:" + finalSession.state());
  System.out.println("-------------------------------\n");
}
```

## Full Code Example

Complete self-contained runnable class combining all parts above.

```java
// Full runnable code for the StoryFlowAgent example

import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.InvocationContext;
import com.google.adk.agents.LoopAgent;
import com.google.adk.agents.SequentialAgent;
import com.google.adk.events.Event;
import com.google.adk.runner.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.genai.types.Content;
import com.google.genai.types.Part;
import io.reactivex.rxjava3.core.Flowable;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.logging.Level;
import java.util.logging.Logger;

public class StoryFlowAgentExample extends BaseAgent {

  // --- Constants ---
  private static final String APP_NAME = "story_app";
  private static final String USER_ID = "user_12345";
  private static final String SESSION_ID = "session_123344";
  private static final String MODEL_NAME = "gemini-2.0-flash";

  private static final Logger logger = Logger.getLogger(StoryFlowAgentExample.class.getName());

  private final LlmAgent storyGenerator;
  private final LoopAgent loopAgent;
  private final SequentialAgent sequentialAgent;

  public StoryFlowAgentExample(
      String name, LlmAgent storyGenerator, LoopAgent loopAgent, SequentialAgent sequentialAgent) {
    super(
        name,
        "Orchestrates story generation, critique, revision, and checks.",
        List.of(storyGenerator, loopAgent, sequentialAgent),
        null,
        null);

    this.storyGenerator = storyGenerator;
    this.loopAgent = loopAgent;
    this.sequentialAgent = sequentialAgent;
  }

  public static void main(String[] args) {

    // --- Define the individual LLM agents ---
    LlmAgent storyGenerator =
        LlmAgent.builder()
            .name("StoryGenerator")
            .model(MODEL_NAME)
            .description("Generates the initial story.")
            .instruction(
                """
              You are a story writer. Write a short story (around 100 words) about a cat,
              based on the topic: {topic}
              """)
            .inputSchema(null)
            .outputKey("current_story")
            .build();

    LlmAgent critic =
        LlmAgent.builder()
            .name("Critic")
            .model(MODEL_NAME)
            .description("Critiques the story.")
            .instruction(
                """
              You are a story critic. Review the story: {current_story}. Provide 1-2 sentences of constructive criticism
              on how to improve it. Focus on plot or character.
              """)
            .inputSchema(null)
            .outputKey("criticism")
            .build();

    LlmAgent reviser =
        LlmAgent.builder()
            .name("Reviser")
            .model(MODEL_NAME)
            .description("Revises the story based on criticism.")
            .instruction(
                """
              You are a story reviser. Revise the story: {current_story}, based on the criticism: {criticism}. Output only the revised story.
              """)
            .inputSchema(null)
            .outputKey("current_story")
            .build();

    LlmAgent grammarCheck =
        LlmAgent.builder()
            .name("GrammarCheck")
            .model(MODEL_NAME)
            .description("Checks grammar and suggests corrections.")
            .instruction(
                """
               You are a grammar checker. Check the grammar of the story: {current_story}. Output only the suggested
               corrections as a list, or output 'Grammar is good!' if there are no errors.
               """)
            .outputKey("grammar_suggestions")
            .build();

    LlmAgent toneCheck =
        LlmAgent.builder()
            .name("ToneCheck")
            .model(MODEL_NAME)
            .description("Analyzes the tone of the story.")
            .instruction(
                """
              You are a tone analyzer. Analyze the tone of the story: {current_story}. Output only one word: 'positive' if
              the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral'
              otherwise.
              """)
            .outputKey("tone_check_result")
            .build();

    LoopAgent loopAgent =
        LoopAgent.builder()
            .name("CriticReviserLoop")
            .description("Iteratively critiques and revises the story.")
            .subAgents(critic, reviser)
            .maxIterations(2)
            .build();

    SequentialAgent sequentialAgent =
        SequentialAgent.builder()
            .name("PostProcessing")
            .description("Performs grammar and tone checks sequentially.")
            .subAgents(grammarCheck, toneCheck)
            .build();

    StoryFlowAgentExample storyFlowAgentExample =
        new StoryFlowAgentExample(APP_NAME, storyGenerator, loopAgent, sequentialAgent);

    // --- Run the Agent ---
    runAgent(storyFlowAgentExample, "a lonely robot finding a friend in a junkyard");
  }

  // --- Function to Interact with the Agent ---
  public static void runAgent(StoryFlowAgentExample agent, String userTopic) {
    // --- Setup Runner and Session ---
    InMemoryRunner runner = new InMemoryRunner(agent);

    Map<String, Object> initialState = new HashMap<>();
    initialState.put("topic", "a brave kitten exploring a haunted house");

    Session session =
        runner
            .sessionService()
            .createSession(APP_NAME, USER_ID, new ConcurrentHashMap<>(initialState), SESSION_ID)
            .blockingGet();
    logger.log(Level.INFO, () -> String.format("Initial session state: %s", session.state()));

    session.state().put("topic", userTopic);
    logger.log(Level.INFO, () -> String.format("Updated session state topic to: %s", userTopic));

    Content userMessage = Content.fromParts(Part.fromText("Generate a story about: " + userTopic));
    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);

    final String[] finalResponse = {"No final response captured."};
    eventStream.blockingForEach(
        event -> {
          if (event.finalResponse() && event.content().isPresent()) {
            String author = event.author() != null ? event.author() : "UNKNOWN_AUTHOR";
            Optional<String> textOpt =
                event
                    .content()
                    .flatMap(Content::parts)
                    .filter(parts -> !parts.isEmpty())
                    .map(parts -> parts.get(0).text().orElse(""));

            logger.log(Level.INFO, () ->
                String.format("Potential final response from [%s]: %s", author, textOpt.orElse("N/A")));
            textOpt.ifPresent(text -> finalResponse[0] = text);
          }
        });

    System.out.println("\n--- Agent Interaction Result ---");
    System.out.println("Agent Final Response: " + finalResponse[0]);

    Session finalSession =
        runner
            .sessionService()
            .getSession(APP_NAME, USER_ID, SESSION_ID, Optional.empty())
            .blockingGet();

    assert finalSession != null;
    System.out.println("Final Session State:" + finalSession.state());
    System.out.println("-------------------------------\n");
  }

  private boolean isStoryGenerated(InvocationContext ctx) {
    Object currentStoryObj = ctx.session().state().get("current_story");
    return currentStoryObj != null && !String.valueOf(currentStoryObj).isEmpty();
  }

  @Override
  protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
    logger.log(Level.INFO, () -> String.format("[%s] Starting story generation workflow.", name()));

    // Stage 1. Initial Story Generation
    Flowable<Event> storyGenFlow = runStage(storyGenerator, invocationContext, "StoryGenerator");

    // Stage 2: Critic-Reviser Loop (runs after story generation completes)
    Flowable<Event> criticReviserFlow = Flowable.defer(() -> {
      if (!isStoryGenerated(invocationContext)) {
        logger.log(Level.SEVERE,() ->
            String.format("[%s] Failed to generate initial story. Aborting after StoryGenerator.",
                name()));
        return Flowable.empty();
      }
        logger.log(Level.INFO, () ->
            String.format("[%s] Story state after generator: %s",
                name(), invocationContext.session().state().get("current_story")));
        return runStage(loopAgent, invocationContext, "CriticReviserLoop");
    });

    // Stage 3: Post-Processing (runs after critic-reviser loop completes)
    Flowable<Event> postProcessingFlow = Flowable.defer(() -> {
      logger.log(Level.INFO, () ->
          String.format("[%s] Story state after loop: %s",
              name(), invocationContext.session().state().get("current_story")));
      return runStage(sequentialAgent, invocationContext, "PostProcessing");
    });

    // Stage 4: Conditional Regeneration (runs after post-processing completes)
    Flowable<Event> conditionalRegenFlow = Flowable.defer(() -> {
      String toneCheckResult = (String) invocationContext.session().state().get("tone_check_result");
      logger.log(Level.INFO, () -> String.format("[%s] Tone check result: %s", name(), toneCheckResult));

      if ("negative".equalsIgnoreCase(toneCheckResult)) {
        logger.log(Level.INFO, () ->
            String.format("[%s] Tone is negative. Regenerating story...", name()));
        return runStage(storyGenerator, invocationContext, "StoryGenerator (Regen)");
      } else {
        logger.log(Level.INFO, () ->
            String.format("[%s] Tone is not negative. Keeping current story.", name()));
        return Flowable.empty();
      }
    });

    return Flowable.concatArray(storyGenFlow, criticReviserFlow, postProcessingFlow, conditionalRegenFlow)
        .doOnComplete(() -> logger.log(Level.INFO, () -> String.format("[%s] Workflow finished.", name())));
  }

  private Flowable<Event> runStage(BaseAgent agentToRun, InvocationContext ctx, String stageName) {
    logger.log(Level.INFO, () -> String.format("[%s] Running %s...", name(), stageName));
    return agentToRun
        .runAsync(ctx)
        .doOnNext(event ->
            logger.log(Level.INFO,() ->
                String.format("[%s] Event from %s: %s", name(), stageName, event.toJson())))
        .doOnError(err ->
            logger.log(Level.SEVERE,
                String.format("[%s] Error in %s", name(), stageName), err))
        .doOnComplete(() ->
            logger.log(Level.INFO, () ->
                String.format("[%s] %s finished.", name(), stageName)));
  }

  @Override
  protected Flowable<Event> runLiveImpl(InvocationContext invocationContext) {
    return Flowable.error(new UnsupportedOperationException("runLive not implemented."));
  }
}
```
