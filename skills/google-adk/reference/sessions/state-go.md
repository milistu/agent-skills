# Session State — Go Examples

## 1. `{key}` Templating in Agent Instructions

Inject session state values directly into an agent's instruction string using `{key}` placeholders.
Create the session with the desired state key set, then reference it in the instruction.

```go
func keyTemplatingExample() {
    ctx := context.Background()
    sessionService := session.InMemoryService()

    // Create a session with 'topic' in its state.
    _, err := sessionService.Create(ctx, &session.CreateRequest{
        AppName:   appName,
        UserID:    userID,
        SessionID: sessionID,
        State: map[string]any{
            "topic": "friendship",
        },
    })
    if err != nil {
        log.Fatalf("Failed to create session: %v", err)
    }

    // The ADK automatically injects session state into the instruction
    // before calling the LLM. {topic} becomes "friendship".
    model, err := gemini.NewModel(ctx, modelID, nil)
    if err != nil {
        log.Fatalf("Failed to create Gemini model: %v", err)
    }
    storyGenerator, err := llmagent.New(llmagent.Config{
        Name:        "StoryGenerator",
        Model:       model,
        Instruction: "Write a short story about a cat, focusing on the theme: {topic}.",
        // Use {topic?} for an optional key that may not be present.
    })
    if err != nil {
        log.Fatalf("Failed to create agent: %v", err)
    }

    r, err := runner.New(runner.Config{
        AppName:        appName,
        Agent:          agent.Agent(storyGenerator),
        SessionService: sessionService,
    })
    if err != nil {
        log.Fatalf("Failed to create runner: %v", err)
    }
    _ = r
}
```

## 2. `InstructionProvider` Function — Literal Curly Braces

When instructions contain literal curly braces, use a provider function. The ADK will not attempt
state injection; the returned string is passed to the model as-is.

```go
// staticInstructionProvider returns a string with literal braces.
// Because it is a provider function (not a plain string), the ADK will not
// attempt state injection, preserving the literal braces.
func staticInstructionProvider(ctx agent.ReadonlyContext) (string, error) {
    return `Format your output as JSON: {"city": "<name>", "population": <number>}`, nil
}

func instructionProviderExample() {
    ctx := context.Background()
    model, err := gemini.NewModel(ctx, modelID, nil)
    if err != nil {
        log.Fatalf("Failed to create model: %v", err)
    }
    a, err := llmagent.New(llmagent.Config{
        Name:                "template_helper_agent",
        Model:               model,
        InstructionProvider: staticInstructionProvider,
    })
    if err != nil {
        log.Fatalf("Failed to create agent: %v", err)
    }
    _ = a
}
```

## 3. `instructionutil.InjectSessionState` Utility with `InstructionProvider`

Use `instructionutil.InjectSessionState` to selectively inject state into a template string
while leaving non-identifier curly brace expressions untouched.

```go
// dynamicInstructionProvider injects the 'adjective' state variable but
// preserves {{literal_braces}} because their content is not a valid identifier.
func dynamicInstructionProvider(ctx agent.ReadonlyContext) (string, error) {
    template := "This is a {adjective} instruction with {{literal_braces}}."
    return instructionutil.InjectSessionState(ctx, template)
}

func dynamicInstructionExample() {
    ctx := context.Background()
    model, err := gemini.NewModel(ctx, modelID, nil)
    if err != nil {
        log.Fatalf("Failed to create model: %v", err)
    }
    a, err := llmagent.New(llmagent.Config{
        Name:                "dynamic_template_helper_agent",
        Model:               model,
        InstructionProvider: dynamicInstructionProvider,
    })
    if err != nil {
        log.Fatalf("Failed to create agent: %v", err)
    }
    _ = a
}
```

## 4. `OutputKey` → `session.Get()` → `State().Get()` Round-Trip

The simplest way to persist an agent's text response into state. The runner uses `OutputKey`
to create the state delta automatically via `AppendEvent`.

```go
func greetingAgentExample(sessionService session.Service) {
    ctx := context.Background()

    model, err := gemini.NewModel(ctx, modelID, nil)
    if err != nil {
        log.Fatalf("Failed to create Gemini model: %v", err)
    }
    greetingAgent, err := llmagent.New(llmagent.Config{
        Name:        "Greeter",
        Model:       model,
        Instruction: "Generate a short, friendly greeting.",
        OutputKey:   "last_greeting", // Saves final response text to state["last_greeting"]
    })
    if err != nil {
        log.Fatalf("Failed to create greeting agent: %v", err)
    }

    r, err := runner.New(runner.Config{
        AppName:        appName,
        Agent:          agent.Agent(greetingAgent),
        SessionService: sessionService,
    })
    if err != nil {
        log.Fatalf("Failed to create runner: %v", err)
    }

    // Run the agent
    userMessage := genai.NewContentFromText("Hello", "user")
    for event, err := range r.Run(ctx, userID, sessionID, userMessage, agent.RunConfig{}) {
        if err != nil {
            log.Printf("Agent Error: %v", err)
            continue
        }
        if isFinalResponse(event) {
            fmt.Println("Agent responded.")
        }
    }

    // Check the updated state
    resp, err := sessionService.Get(ctx, &session.GetRequest{
        AppName: appName, UserID: userID, SessionID: sessionID,
    })
    if err != nil {
        log.Fatalf("Failed to get session: %v", err)
    }
    lastGreeting, _ := resp.Session.State().Get("last_greeting")
    fmt.Printf("State after agent run: last_greeting = %q\n", lastGreeting)
}
```

## 5. `EventActions.StateDelta` — Manual State Update via `AppendEvent`

For complex updates: multiple keys, non-string values, scoped prefixes (`user:`, `app:`, `temp:`),
or updates not tied to an agent's final text response.

```go
func manualStateUpdateExample(sessionService session.Service) {
    ctx := context.Background()

    s, err := sessionService.Get(ctx, &session.GetRequest{
        AppName: appName, UserID: userID, SessionID: sessionID,
    })
    if err != nil {
        log.Fatalf("Failed to get session: %v", err)
    }
    retrievedSession := s.Session

    // Read existing value before updating
    loginCount, _ := retrievedSession.State().Get("user:login_count")
    newLoginCount := 1
    if lc, ok := loginCount.(int); ok {
        newLoginCount = lc + 1
    }

    stateChanges := map[string]any{
        "task_status":            "active",            // session-scoped
        "user:login_count":       newLoginCount,        // user-scoped
        "user:last_login_ts":     time.Now().Unix(),    // user-scoped
        "temp:validation_needed": true,                 // temp (discarded after invocation)
    }

    // Create an event with the state delta
    systemEvent := session.NewEvent("inv_login_update")
    systemEvent.Author = "system"
    systemEvent.Actions.StateDelta = stateChanges

    // Append the event to update the state
    if err := sessionService.AppendEvent(ctx, retrievedSession, systemEvent); err != nil {
        log.Fatalf("Failed to append event: %v", err)
    }
    fmt.Println("`AppendEvent` called with explicit state delta.")

    // Check updated state
    updatedResp, err := sessionService.Get(ctx, &session.GetRequest{
        AppName: appName, UserID: userID, SessionID: sessionID,
    })
    if err != nil {
        log.Fatalf("Failed to get session: %v", err)
    }
    taskStatus, _ := updatedResp.Session.State().Get("task_status")
    loginCountVal, _ := updatedResp.Session.State().Get("user:login_count")
    lastLogin, _ := updatedResp.Session.State().Get("user:last_login_ts")
    fmt.Printf("State after event: task_status=%q, user:login_count=%v, user:last_login_ts=%v\n",
        taskStatus, loginCountVal, lastLogin)
    // Note: 'temp:validation_needed' is NOT present (discarded after invocation).
}
```

## 6. `agent.CallbackContext` State Mutation (Tool Functions)

The recommended way to mutate state from within tool functions. Changes made via the context's
`State()` methods are automatically captured into the event's `StateDelta`.

```go
func contextStateUpdateExample(sessionService session.Service) {
    ctx := context.Background()

    updateActionCountTool, err := functiontool.New(
        functiontool.Config{
            Name:        "update_action_count",
            Description: "Updates the user action count in the state.",
        },
        func(tctx tool.Context, args struct{}) (struct{}, error) {
            actx, ok := tctx.(agent.CallbackContext)
            if !ok {
                return struct{}{}, fmt.Errorf("tool.Context is not of type agent.CallbackContext")
            }

            // Read then update an existing state value
            s, _ := actx.State().Get("user_action_count")
            newCount := 1
            if c, ok := s.(int); ok {
                newCount = c + 1
            }
            if err := actx.State().Set("user_action_count", newCount); err != nil {
                log.Printf("could not set user_action_count: %v", err)
            }

            // Add a temporary value (discarded after the invocation ends)
            if err := actx.State().Set("temp:last_operation_status", "success"); err != nil {
                log.Printf("could not set temp:last_operation_status: %v", err)
            }

            // Changes are automatically part of the event's StateDelta —
            // no manual EventActions construction needed.
            return struct{}{}, nil
        },
    )
    if err != nil {
        log.Fatalf("Failed to create tool: %v", err)
    }

    model, err := gemini.NewModel(ctx, modelID, nil)
    if err != nil {
        log.Fatalf("Failed to create model: %v", err)
    }
    toolAgent, err := llmagent.New(llmagent.Config{
        Name:        "ToolAgent",
        Model:       model,
        Instruction: "Use the update_action_count tool.",
        Tools:       []tool.Tool{updateActionCountTool},
    })
    if err != nil {
        log.Fatalf("Failed to create tool agent: %v", err)
    }

    r, err := runner.New(runner.Config{
        AppName:        appName,
        Agent:          agent.Agent(toolAgent),
        SessionService: sessionService,
    })
    if err != nil {
        log.Fatalf("Failed to create runner: %v", err)
    }

    userMessage := genai.NewContentFromText("Please update the action count.", "user")
    for _, err := range r.Run(ctx, userID, sessionID, userMessage, agent.RunConfig{}) {
        if err != nil {
            log.Printf("Agent Error: %v", err)
        }
    }

    resp, err := sessionService.Get(ctx, &session.GetRequest{
        AppName: appName, UserID: userID, SessionID: sessionID,
    })
    if err != nil {
        log.Fatalf("Failed to get session: %v", err)
    }
    actionCount, _ := resp.Session.State().Get("user_action_count")
    fmt.Printf("State after tool run: user_action_count = %v\n", actionCount)
}
```
