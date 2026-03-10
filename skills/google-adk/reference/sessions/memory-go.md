# Memory Service — Go Examples

## 1. InMemoryMemoryService: add_session_to_memory, custom memory tool, two-runner cross-session recall

```go
package main

import (
    "context"
    "fmt"
    "log"
    "strings"

    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/memory"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/adk/runner"
    "google.golang.org/adk/session"
    "google.golang.org/adk/tool"
    "google.golang.org/adk/tool/functiontool"
    "google.golang.org/genai"
)

const (
    appName = "go_memory_example_app"
    userID  = "go_mem_user"
    modelID = "gemini-2.5-pro"
)

// Args defines the input structure for the memory search tool.
type Args struct {
    Query string `json:"query" jsonschema:"The query to search for in the memory."`
}

// Result defines the output structure for the memory search tool.
type Result struct {
    Results []string `json:"results"`
}

// memorySearchToolFunc accesses memory via tool.Context.SearchMemory.
func memorySearchToolFunc(tctx tool.Context, args Args) (Result, error) {
    fmt.Printf("Tool: Searching memory for query: '%s'\n", args.Query)
    searchResults, err := tctx.SearchMemory(context.Background(), args.Query)
    if err != nil {
        log.Printf("Error searching memory: %v", err)
        return Result{}, fmt.Errorf("failed memory search")
    }

    var results []string
    for _, res := range searchResults.Memories {
        if res.Content != nil {
            results = append(results, textParts(res.Content)...)
        }
    }
    return Result{Results: results}, nil
}

// memorySearchTool wraps memorySearchToolFunc as a named ADK tool.
var memorySearchTool = must(functiontool.New(
    functiontool.Config{
        Name:        "search_past_conversations",
        Description: "Searches past conversations for relevant information.",
    },
    memorySearchToolFunc,
))

func main() {
    ctx := context.Background()

    // Services must be shared across runners to share state and memory.
    sessionService := session.InMemoryService()
    memoryService := memory.InMemoryService()

    // --- Scenario 1: Capture information in one session ---
    fmt.Println("--- Turn 1: Capturing Information ---")
    infoCaptureAgent := must(llmagent.New(llmagent.Config{
        Name:        "InfoCaptureAgent",
        Model:       must(gemini.NewModel(ctx, modelID, nil)),
        Instruction: "Acknowledge the user's statement.",
    }))

    runner1 := must(runner.New(runner.Config{
        AppName:        appName,
        Agent:          infoCaptureAgent,
        SessionService: sessionService,
        MemoryService:  memoryService,
    }))

    session1ID := "session_info"
    must(sessionService.Create(ctx, &session.CreateRequest{
        AppName: appName, UserID: userID, SessionID: session1ID,
    }))

    userInput1 := genai.NewContentFromText("My favorite project is Project Alpha.", "user")
    var finalResponseText string
    for event, err := range runner1.Run(ctx, userID, session1ID, userInput1, agent.RunConfig{}) {
        if err != nil {
            log.Printf("Agent 1 Error: %v", err)
            continue
        }
        if event.Content != nil && !event.LLMResponse.Partial {
            finalResponseText = strings.Join(textParts(event.LLMResponse.Content), "")
        }
    }
    fmt.Printf("Agent 1 Response: %s\n", finalResponseText)

    // Add the completed session to the Memory Service
    fmt.Println("\n--- Adding Session 1 to Memory ---")
    resp, err := sessionService.Get(ctx, &session.GetRequest{
        AppName: appName, UserID: userID, SessionID: session1ID,
    })
    if err != nil {
        log.Fatalf("Failed to get completed session: %v", err)
    }
    if err := memoryService.AddSession(ctx, resp.Session); err != nil {
        log.Fatalf("Failed to add session to memory: %v", err)
    }
    fmt.Println("Session added to memory.")

    // --- Scenario 2: Recall the information in a new session using a tool ---
    fmt.Println("\n--- Turn 2: Recalling Information ---")
    memoryRecallAgent := must(llmagent.New(llmagent.Config{
        Name:  "MemoryRecallAgent",
        Model: must(gemini.NewModel(ctx, modelID, nil)),
        Instruction: "Answer the user's question. Use the " +
            "'search_past_conversations' tool if the answer might be in past conversations.",
        Tools: []tool.Tool{memorySearchTool},
    }))

    runner2 := must(runner.New(runner.Config{
        Agent:          memoryRecallAgent,
        AppName:        appName,
        SessionService: sessionService,
        MemoryService:  memoryService,
    }))

    session2ID := "session_recall"
    must(sessionService.Create(ctx, &session.CreateRequest{
        AppName: appName, UserID: userID, SessionID: session2ID,
    }))
    userInput2 := genai.NewContentFromText("What is my favorite project?", "user")

    var finalResponseText2 string
    for event, err := range runner2.Run(ctx, userID, session2ID, userInput2, agent.RunConfig{}) {
        if err != nil {
            log.Printf("Agent 2 Error: %v", err)
            continue
        }
        if event.Content != nil && !event.LLMResponse.Partial {
            finalResponseText2 = strings.Join(textParts(event.LLMResponse.Content), "")
        }
    }
    fmt.Printf("Agent 2 Response: %s\n", finalResponseText2)
}
```

## 2. Searching Memory Within a Tool (via tool.Context)

```go
// memorySearchToolFunc is the implementation of a custom memory search tool.
// It demonstrates accessing the memory service via tool.Context.SearchMemory.
func memorySearchToolFunc(tctx tool.Context, args Args) (Result, error) {
    fmt.Printf("Tool: Searching memory for query: '%s'\n", args.Query)
    // SearchMemory is available on the tool context.
    searchResults, err := tctx.SearchMemory(context.Background(), args.Query)
    if err != nil {
        log.Printf("Error searching memory: %v", err)
        return Result{}, fmt.Errorf("failed memory search")
    }

    var results []string
    for _, res := range searchResults.Memories {
        if res.Content != nil {
            results = append(results, textParts(res.Content)...)
        }
    }
    return Result{Results: results}, nil
}

// Define a tool that wraps the search function.
var memorySearchTool = must(functiontool.New(
    functiontool.Config{
        Name:        "search_past_conversations",
        Description: "Searches past conversations for relevant information.",
    },
    memorySearchToolFunc,
))
```

> **Note:** Go does not yet have a built-in `PreloadMemoryTool` or `VertexAiMemoryBankService` equivalent documented in this source. Use a custom tool wrapping `tctx.SearchMemory` as shown above.
