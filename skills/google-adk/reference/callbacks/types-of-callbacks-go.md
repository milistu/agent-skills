# Callback Types — Go Examples

## before_agent_callback

Checks `skip_llm_agent` in session state. Returns `*genai.Content` to skip the agent, or `nil, nil` to proceed.

```go
package main

import (
    "context"
    "fmt"
    "log"

    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/adk/runner"
    "google.golang.org/adk/session"
    "google.golang.org/genai"
)

const modelName = "gemini-2.0-flash"
const appName = "before_agent_demo"

func onBeforeAgent(ctx agent.CallbackContext) (*genai.Content, error) {
    agentName := ctx.AgentName()
    log.Printf("[Callback] Entering agent: %s", agentName)
    if skip, _ := ctx.State().Get("skip_llm_agent"); skip == true {
        log.Printf("[Callback] State condition met: Skipping agent %s", agentName)
        return genai.NewContentFromText(
            fmt.Sprintf("Agent %s skipped by before_agent_callback.", agentName),
            genai.RoleModel,
        ), nil
    }
    log.Printf("[Callback] State condition not met: Running agent %s", agentName)
    return nil, nil
}

func runBeforeAgentExample() {
    ctx := context.Background()
    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    if err != nil {
        log.Fatalf("FATAL: Failed to create model: %v", err)
    }

    llmCfg := llmagent.Config{
        Name:                 "AgentWithBeforeAgentCallback",
        BeforeAgentCallbacks: []agent.BeforeAgentCallback{onBeforeAgent},
        Model:                geminiModel,
        Instruction:          "You are a concise assistant.",
    }
    testAgent, err := llmagent.New(llmCfg)
    if err != nil {
        log.Fatalf("FATAL: Failed to create agent: %v", err)
    }

    sessionService := session.InMemoryService()
    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    if err != nil {
        log.Fatalf("FATAL: Failed to create runner: %v", err)
    }

    log.Println("--- SCENARIO 1: Agent should run normally ---")
    runScenario(ctx, r, sessionService, appName, "session_normal", nil, "Hello, world!")

    log.Println("\n--- SCENARIO 2: Agent should be skipped ---")
    runScenario(ctx, r, sessionService, appName, "session_skip", map[string]any{"skip_llm_agent": true}, "This should be skipped.")
}
```

## after_agent_callback

Checks `add_concluding_note` in session state. Returns replacement `*genai.Content` or `nil, nil` to pass through the agent's original output.

```go
package main

import (
    "context"
    "log"

    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/adk/runner"
    "google.golang.org/adk/session"
    "google.golang.org/genai"
)

func onAfterAgent(ctx agent.CallbackContext) (*genai.Content, error) {
    agentName := ctx.AgentName()
    invocationID := ctx.InvocationID()
    state := ctx.State()

    log.Printf("\n[Callback] Exiting agent: %s (Inv: %s)", agentName, invocationID)
    log.Printf("[Callback] Current State: %v", state)

    if addNote, _ := state.Get("add_concluding_note"); addNote == true {
        log.Printf("[Callback] Replacing agent %s's output.", agentName)
        return genai.NewContentFromText(
            "Concluding note added by after_agent_callback, replacing original output.",
            genai.RoleModel,
        ), nil
    }

    log.Printf("[Callback] Using agent %s's original output.", agentName)
    return nil, nil
}

func runAfterAgentExample() {
    ctx := context.Background()
    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    if err != nil {
        log.Fatalf("FATAL: Failed to create model: %v", err)
    }

    llmCfg := llmagent.Config{
        Name:                "AgentWithAfterAgentCallback",
        AfterAgentCallbacks: []agent.AfterAgentCallback{onAfterAgent},
        Model:               geminiModel,
        Instruction:         "You are a simple agent. Just say 'Processing complete!'",
    }
    testAgent, err := llmagent.New(llmCfg)
    if err != nil {
        log.Fatalf("FATAL: Failed to create agent: %v", err)
    }

    sessionService := session.InMemoryService()
    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    if err != nil {
        log.Fatalf("FATAL: Failed to create runner: %v", err)
    }

    log.Println("--- SCENARIO 1: Should use original output ---")
    runScenario(ctx, r, sessionService, appName, "session_normal", nil, "Process this.")

    log.Println("\n--- SCENARIO 2: Should replace output ---")
    runScenario(ctx, r, sessionService, appName, "session_modify", map[string]any{"add_concluding_note": true}, "Process and add note.")
}
```

## before_model_callback

Mutates `req.Config.SystemInstruction` (adds a prefix) and returns a `*model.LLMResponse` to block the call when "BLOCK" appears in the user message, or `nil, nil` to proceed.

```go
package main

import (
    "context"
    "log"
    "strings"

    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/model"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/adk/runner"
    "google.golang.org/adk/session"
    "google.golang.org/genai"
)

func onBeforeModel(ctx agent.CallbackContext, req *model.LLMRequest) (*model.LLMResponse, error) {
    log.Printf("[Callback] BeforeModel triggered for agent %q.", ctx.AgentName())

    // Modification: prefix the system instruction
    if req.Config.SystemInstruction != nil {
        prefix := "[Modified by Callback] "
        if len(req.Config.SystemInstruction.Parts) > 0 {
            req.Config.SystemInstruction.Parts[0].Text = prefix + req.Config.SystemInstruction.Parts[0].Text
        } else {
            req.Config.SystemInstruction.Parts = append(req.Config.SystemInstruction.Parts, &genai.Part{Text: prefix})
        }
        log.Printf("[Callback] Modified system instruction.")
    }

    // Skip: block if user message contains "BLOCK"
    for _, content := range req.Contents {
        for _, part := range content.Parts {
            if strings.Contains(strings.ToUpper(part.Text), "BLOCK") {
                log.Println("[Callback] 'BLOCK' keyword found. Skipping LLM call.")
                return &model.LLMResponse{
                    Content: &genai.Content{
                        Parts: []*genai.Part{{Text: "LLM call was blocked by before_model_callback."}},
                        Role:  "model",
                    },
                }, nil
            }
        }
    }

    log.Println("[Callback] Proceeding with LLM call.")
    return nil, nil
}

func runBeforeModelExample() {
    ctx := context.Background()
    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    if err != nil {
        log.Fatalf("FATAL: Failed to create model: %v", err)
    }

    llmCfg := llmagent.Config{
        Name:                 "AgentWithBeforeModelCallback",
        Model:                geminiModel,
        BeforeModelCallbacks: []llmagent.BeforeModelCallback{onBeforeModel},
    }
    testAgent, err := llmagent.New(llmCfg)
    if err != nil {
        log.Fatalf("FATAL: Failed to create agent: %v", err)
    }

    sessionService := session.InMemoryService()
    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    if err != nil {
        log.Fatalf("FATAL: Failed to create runner: %v", err)
    }

    log.Println("--- SCENARIO 1: Should proceed to LLM ---")
    runScenario(ctx, r, sessionService, appName, "session_normal", nil, "Tell me a fun fact.")

    log.Println("\n--- SCENARIO 2: Should be blocked by callback ---")
    runScenario(ctx, r, sessionService, appName, "session_blocked", nil, "write a joke on BLOCK")
}
```

## after_model_callback

Inspects the response text and replaces "joke" with "funny story" using a case-insensitive regex. Returns the mutated response or `nil, nil` to pass through unchanged.

```go
package main

import (
    "context"
    "log"
    "regexp"
    "strings"

    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/model"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/adk/runner"
    "google.golang.org/adk/session"
    "google.golang.org/genai"
)

func onAfterModel(ctx agent.CallbackContext, resp *model.LLMResponse, respErr error) (*model.LLMResponse, error) {
    log.Printf("[Callback] AfterModel triggered for agent %q.", ctx.AgentName())
    if respErr != nil {
        log.Printf("[Callback] Model returned an error: %v. Passing it through.", respErr)
        return nil, respErr
    }
    if resp == nil || resp.Content == nil || len(resp.Content.Parts) == 0 {
        log.Println("[Callback] Response is nil or has no parts.")
        return nil, nil
    }
    if resp.Content.Parts[0].FunctionCall != nil {
        log.Println("[Callback] Response is a function call. No modification.")
        return nil, nil
    }

    originalText := resp.Content.Parts[0].Text
    re := regexp.MustCompile(`(?i)\bjoke\b`)
    if !re.MatchString(originalText) {
        log.Println("[Callback] 'joke' not found. Passing original response through.")
        return nil, nil
    }

    log.Println("[Callback] 'joke' found. Modifying response.")
    modifiedText := re.ReplaceAllStringFunc(originalText, func(s string) string {
        if s == "Joke" {
            return "Funny story"
        }
        return "funny story"
    })
    _ = strings.ToLower // imported for other examples

    resp.Content.Parts[0].Text = modifiedText
    return resp, nil
}

func runAfterModelExample() {
    ctx := context.Background()
    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    if err != nil {
        log.Fatalf("FATAL: Failed to create model: %v", err)
    }

    llmCfg := llmagent.Config{
        Name:                "AgentWithAfterModelCallback",
        Model:               geminiModel,
        AfterModelCallbacks: []llmagent.AfterModelCallback{onAfterModel},
    }
    testAgent, err := llmagent.New(llmCfg)
    if err != nil {
        log.Fatalf("FATAL: Failed to create agent: %v", err)
    }

    sessionService := session.InMemoryService()
    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    if err != nil {
        log.Fatalf("FATAL: Failed to create runner: %v", err)
    }

    log.Println("--- SCENARIO 1: Response should be modified ---")
    runScenario(ctx, r, sessionService, appName, "session_modify", nil, "Give me a paragraph about different styles of jokes.")
}
```

## before_tool_callback

Modifies tool `args` (redirects "canada" to "France") or returns a result map to skip tool execution entirely when "BLOCK" is passed.

```go
package main

import (
    "context"
    "fmt"
    "log"
    "strings"

    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/adk/runner"
    "google.golang.org/adk/session"
    "google.golang.org/adk/tool"
    "google.golang.org/adk/tool/functiontool"
    "google.golang.org/genai"
)

type GetCapitalCityArgs struct {
    Country string `json:"country" jsonschema:"The country to get the capital of."`
}

func getCapitalCity(ctx tool.Context, args *GetCapitalCityArgs) (string, error) {
    capitals := map[string]string{
        "canada":        "Ottawa",
        "france":        "Paris",
        "germany":       "Berlin",
        "united states": "Washington, D.C.",
    }
    capital, ok := capitals[strings.ToLower(args.Country)]
    if !ok {
        return "", fmt.Errorf("unknown country: %s", args.Country)
    }
    return capital, nil
}

func onBeforeTool(ctx tool.Context, t tool.Tool, args map[string]any) (map[string]any, error) {
    log.Printf("[Callback] BeforeTool triggered for tool %q in agent %q.", t.Name(), ctx.AgentName())
    log.Printf("[Callback] Original args: %v", args)

    if t.Name() == "getCapitalCity" {
        if country, ok := args["country"].(string); ok {
            if strings.ToLower(country) == "canada" {
                log.Println("[Callback] Detected 'Canada'. Modifying args to 'France'.")
                args["country"] = "France"
                return args, nil // proceed with modified args
            } else if strings.ToUpper(country) == "BLOCK" {
                log.Println("[Callback] Detected 'BLOCK'. Skipping tool execution.")
                return map[string]any{"result": "Tool execution was blocked by before_tool_callback."}, nil
            }
        }
    }
    log.Println("[Callback] Proceeding with original or previously modified args.")
    return nil, nil
}

func runBeforeToolExample() {
    ctx := context.Background()
    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    if err != nil {
        log.Fatalf("FATAL: Failed to create model: %v", err)
    }
    capitalTool, err := functiontool.New(functiontool.Config{
        Name:        "getCapitalCity",
        Description: "Retrieves the capital city of a given country.",
    }, getCapitalCity)
    if err != nil {
        log.Fatalf("FATAL: Failed to create function tool: %v", err)
    }

    llmCfg := llmagent.Config{
        Name:                "AgentWithBeforeToolCallback",
        Model:               geminiModel,
        Tools:               []tool.Tool{capitalTool},
        BeforeToolCallbacks: []llmagent.BeforeToolCallback{onBeforeTool},
        Instruction:         "You are an agent that can find capital cities. Use the getCapitalCity tool.",
    }
    testAgent, err := llmagent.New(llmCfg)
    if err != nil {
        log.Fatalf("FATAL: Failed to create agent: %v", err)
    }
    sessionService := session.InMemoryService()
    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    if err != nil {
        log.Fatalf("FATAL: Failed to create runner: %v", err)
    }

    log.Println("--- SCENARIO 1: Args should be modified ---")
    runScenario(ctx, r, sessionService, appName, "session_tool_modify", nil, "What is the capital of Canada?")

    log.Println("--- SCENARIO 2: Tool call should be blocked ---")
    runScenario(ctx, r, sessionService, appName, "session_tool_block", nil, "capital of BLOCK")
}
```

## after_tool_callback

Inspects the tool result map and appends a note when the capital is "Washington, D.C.". Returns the modified map or `nil, nil` to pass through the original.

```go
package main

import (
    "context"
    "fmt"
    "log"
    "strings"

    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/adk/runner"
    "google.golang.org/adk/session"
    "google.golang.org/adk/tool"
    "google.golang.org/adk/tool/functiontool"
    "google.golang.org/genai"
)

func onAfterTool(ctx tool.Context, t tool.Tool, args map[string]any, result map[string]any, err error) (map[string]any, error) {
    log.Printf("[Callback] AfterTool triggered for tool %q in agent %q.", t.Name(), ctx.AgentName())
    log.Printf("[Callback] Original result: %v", result)

    if err != nil {
        log.Printf("[Callback] Tool run produced an error: %v. Passing through.", err)
        return nil, err
    }

    if t.Name() == "getCapitalCity" {
        if originalResult, ok := result["result"].(string); ok && originalResult == "Washington, D.C." {
            log.Println("[Callback] Detected 'Washington, D.C.'. Modifying tool response.")
            modifiedResult := make(map[string]any)
            for k, v := range result {
                modifiedResult[k] = v
            }
            modifiedResult["result"] = fmt.Sprintf("%s (Note: This is the capital of the USA).", originalResult)
            modifiedResult["note_added_by_callback"] = true
            return modifiedResult, nil
        }
    }

    log.Println("[Callback] Passing original tool response through.")
    return nil, nil
}

func runAfterToolExample() {
    ctx := context.Background()
    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    if err != nil {
        log.Fatalf("FATAL: Failed to create model: %v", err)
    }
    capitalTool, err := functiontool.New(functiontool.Config{
        Name:        "getCapitalCity",
        Description: "Retrieves the capital city of a given country.",
    }, getCapitalCity)
    if err != nil {
        log.Fatalf("FATAL: Failed to create function tool: %v", err)
    }

    llmCfg := llmagent.Config{
        Name:               "AgentWithAfterToolCallback",
        Model:              geminiModel,
        Tools:              []tool.Tool{capitalTool},
        AfterToolCallbacks: []llmagent.AfterToolCallback{onAfterTool},
        Instruction:        "You are an agent that finds capital cities. Use the getCapitalCity tool.",
    }
    testAgent, err := llmagent.New(llmCfg)
    if err != nil {
        log.Fatalf("FATAL: Failed to create agent: %v", err)
    }
    sessionService := session.InMemoryService()
    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    if err != nil {
        log.Fatalf("FATAL: Failed to create runner: %v", err)
    }

    log.Println("--- SCENARIO 1: Result should be modified ---")
    runScenario(ctx, r, sessionService, appName, "session_tool_after_modify", nil, "capital of united states")
}
```
