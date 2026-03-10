# Function Tools — Go Examples

## Required Parameters

A Go struct where all fields lack `omitempty`/`omitzero` — both `Location` and `Unit` are required by the LLM.

```go
// GetWeatherParams defines the arguments for the getWeather tool.
type GetWeatherParams struct {
    // This field is REQUIRED (no "omitempty").
    // The jsonschema tag provides the description.
    Location string `json:"location" jsonschema:"The city and state, e.g., San Francisco, CA"`

    // This field is also REQUIRED.
    Unit string `json:"unit" jsonschema:"The temperature unit, either 'celsius' or 'fahrenheit'"`
}
```

## Optional Parameters

Adding `omitempty` or `omitzero` to the `json` tag makes a field optional; the LLM may omit it.

```go
// GetWeatherParams defines the arguments for the getWeather tool.
type GetWeatherParams struct {
    // Location is required.
    Location string `json:"location" jsonschema:"The city and state, e.g., San Francisco, CA"`

    // Unit is optional.
    Unit string `json:"unit,omitempty" jsonschema:"The temperature unit, either 'celsius' or 'fahrenheit'"`

    // Days is optional.
    Days int `json:"days,omitzero" jsonschema:"The number of forecast days to return (defaults to 1)"`
}
```

## Function Tool Example — Stock Price Agent

Full working example: `getStockPrice` is wrapped with `functiontool.New` and registered on an `llmagent`. Includes session setup and a multi-prompt simulation loop.

```go
package main

import (
    "context"
    "fmt"
    "log"
    "strings"

    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/adk/runner"
    "google.golang.org/adk/session"
    "google.golang.org/adk/tool"
    "google.golang.org/adk/tool/functiontool"

    "google.golang.org/genai"
)

// mockStockPrices simulates a stock data API without network calls.
var mockStockPrices = map[string]float64{
    "GOOG": 300.6,
    "AAPL": 123.4,
    "MSFT": 234.5,
}

// getStockPriceArgs defines the schema for the tool's input.
type getStockPriceArgs struct {
    Symbol string `json:"symbol" jsonschema:"The stock ticker symbol, e.g., GOOG"`
}

// getStockPriceResults defines the tool's output schema.
type getStockPriceResults struct {
    Symbol string  `json:"symbol"`
    Price  float64 `json:"price,omitempty"`
    Error  string  `json:"error,omitempty"`
}

// getStockPrice looks up the price in the mock map and returns a typed result.
func getStockPrice(ctx tool.Context, input getStockPriceArgs) (getStockPriceResults, error) {
    symbolUpper := strings.ToUpper(input.Symbol)
    if price, ok := mockStockPrices[symbolUpper]; ok {
        fmt.Printf("Tool: Found price for %s: %f\n", input.Symbol, price)
        return getStockPriceResults{Symbol: input.Symbol, Price: price}, nil
    }
    return getStockPriceResults{}, fmt.Errorf("no data found for symbol")
}

// createStockAgent builds an LlmAgent equipped with the getStockPrice tool.
func createStockAgent(ctx context.Context) (agent.Agent, error) {
    stockPriceTool, err := functiontool.New(
        functiontool.Config{
            Name:        "get_stock_price",
            Description: "Retrieves the current stock price for a given symbol.",
        },
        getStockPrice)
    if err != nil {
        return nil, err
    }

    model, err := gemini.NewModel(ctx, "gemini-2.5-flash", &genai.ClientConfig{})
    if err != nil {
        log.Fatalf("Failed to create model: %v", err)
    }

    return llmagent.New(llmagent.Config{
        Name:        "stock_agent",
        Model:       model,
        Instruction: "You are an agent who retrieves stock prices. If a ticker symbol is provided, fetch the current price. If only a company name is given, first perform a Google search to find the correct ticker symbol before retrieving the stock price. If the provided ticker symbol is invalid or data cannot be retrieved, inform the user that the stock price could not be found.",
        Description: "This agent specializes in retrieving real-time stock prices.",
        Tools:       []tool.Tool{stockPriceTool},
    })
}

const (
    userID  = "example_user_id"
    appName = "example_app"
)

// callAgent sets up a session and runner, then streams the agent's response.
func callAgent(ctx context.Context, a agent.Agent, prompt string) {
    sessionService := session.InMemoryService()
    sess, err := sessionService.Create(ctx, &session.CreateRequest{
        AppName: appName,
        UserID:  userID,
    })
    if err != nil {
        log.Fatalf("Failed to create the session service: %v", err)
    }
    config := runner.Config{
        AppName:        appName,
        Agent:          a,
        SessionService: sessionService,
    }
    r, err := runner.New(config)
    if err != nil {
        log.Fatalf("Failed to create the runner: %v", err)
    }

    sessionID := sess.Session.ID()
    userMsg := &genai.Content{
        Parts: []*genai.Part{genai.NewPartFromText(prompt)},
        Role:  string(genai.RoleUser),
    }

    for event, err := range r.Run(ctx, userID, sessionID, userMsg, agent.RunConfig{
        StreamingMode: agent.StreamingModeNone,
    }) {
        if err != nil {
            fmt.Printf("\nAGENT_ERROR: %v\n", err)
        } else {
            for _, p := range event.Content.Parts {
                fmt.Print(p.Text)
            }
        }
    }
}

func RunAgentSimulation() {
    a, err := createStockAgent(context.Background())
    if err != nil {
        panic(err)
    }
    fmt.Println("Agent created:", a.Name())
    prompts := []string{
        "stock price of GOOG",
        "What's the price of MSFT?",
        "Can you find the stock price for an unknown company XYZ?",
    }
    for _, prompt := range prompts {
        fmt.Printf("\nPrompt: %s\nResponse: ", prompt)
        callAgent(context.Background(), a, prompt)
        fmt.Println("\n---")
    }
}

func main() {
    fmt.Println("Attempting to run the agent simulation...")
    RunAgentSimulation()
}
```

## LongRunningFunctionTool — Creating the Tool

`createTicketAsync` returns an initial `CreateTicketResults` struct (with a ticket ID); wrapping it with `functiontool.New` inside `createTicketAgent` registers it as a long-running tool.

```go
import (
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/adk/tool"
    "google.golang.org/adk/tool/functiontool"
    "google.golang.org/genai"
)

// CreateTicketArgs defines the arguments for our long-running tool.
type CreateTicketArgs struct {
    Urgency string `json:"urgency" jsonschema:"The urgency level of the ticket."`
}

// CreateTicketResults defines the *initial* output of our long-running tool.
type CreateTicketResults struct {
    Status   string `json:"status"`
    TicketId string `json:"ticket_id"`
}

// createTicketAsync simulates the initiation of a long-running ticket creation task.
// It returns the ticket ID in the initial response so the client can track progress.
func createTicketAsync(ctx tool.Context, args CreateTicketArgs) (CreateTicketResults, error) {
    log.Printf("TOOL_EXEC: 'create_ticket_long_running' called with urgency: %s (Call ID: %s)\n", args.Urgency, ctx.FunctionCallID())

    ticketID := "TICKET-ABC-123"
    log.Printf("ACTION: Generated Ticket ID: %s for Call ID: %s\n", ticketID, ctx.FunctionCallID())

    return CreateTicketResults{
        Status:   "started",
        TicketId: ticketID,
    }, nil
}

func createTicketAgent(ctx context.Context) (agent.Agent, error) {
    ticketTool, err := functiontool.New(
        functiontool.Config{
            Name:        "create_ticket_long_running",
            Description: "Creates a new support ticket with a specified urgency level.",
        },
        createTicketAsync,
    )
    if err != nil {
        return nil, fmt.Errorf("failed to create long running tool: %w", err)
    }

    model, err := gemini.NewModel(ctx, "gemini-2.5-flash", &genai.ClientConfig{})
    if err != nil {
        return nil, fmt.Errorf("failed to create model: %v", err)
    }

    return llmagent.New(llmagent.Config{
        Name:        "ticket_agent",
        Model:       model,
        Instruction: "You are a helpful assistant for creating support tickets. Provide the status of the ticket at each interaction.",
        Tools:       []tool.Tool{ticketTool},
    })
}
```

## LongRunningFunctionTool — Intermediate / Final Result Updates (Complete Multi-Turn Example)

`runTurn` captures the function call ID; subsequent turns inject `FunctionResponse` messages back into the runner to simulate async ticket status updates.

```go
// runTurn executes a single turn with the agent and returns the captured function call ID.
func runTurn(ctx context.Context, r *runner.Runner, sessionID, turnLabel string, content *genai.Content) string {
    var funcCallID atomic.Value

    fmt.Printf("\n--- %s ---\n", turnLabel)
    for event, err := range r.Run(ctx, userID, sessionID, content, agent.RunConfig{
        StreamingMode: agent.StreamingModeNone,
    }) {
        if err != nil {
            fmt.Printf("\nAGENT_ERROR: %v\n", err)
            continue
        }
        printEventSummary(event, turnLabel)

        for _, part := range event.Content.Parts {
            if fc := part.FunctionCall; fc != nil {
                if fc.Name == "create_ticket_long_running" {
                    funcCallID.Store(fc.ID)
                }
            }
        }
    }

    if id, ok := funcCallID.Load().(string); ok {
        return id
    }
    return ""
}

func main() {
    ctx := context.Background()
    ticketAgent, err := createTicketAgent(ctx)
    if err != nil {
        log.Fatalf("Failed to create agent: %v", err)
    }

    sessionService := session.InMemoryService()
    sess, err := sessionService.Create(ctx, &session.CreateRequest{AppName: appName, UserID: userID})
    if err != nil {
        log.Fatalf("Failed to create session: %v", err)
    }
    r, err := runner.New(runner.Config{AppName: appName, Agent: ticketAgent, SessionService: sessionService})
    if err != nil {
        log.Fatalf("Failed to create runner: %v", err)
    }

    // --- Turn 1: User requests a ticket ---
    initialUserMessage := genai.NewContentFromText("Create a high urgency ticket for me.", genai.RoleUser)
    funcCallID := runTurn(ctx, r, sess.Session.ID(), "Turn 1: User Request", initialUserMessage)
    if funcCallID == "" {
        log.Fatal("ERROR: Tool 'create_ticket_long_running' not called in Turn 1.")
    }
    fmt.Printf("ACTION: Captured FunctionCall ID: %s\n", funcCallID)

    // --- Turn 2: App provides the final ticket status ---
    ticketID := "TICKET-ABC-123"
    willContinue := false
    ticketStatusResponse := &genai.FunctionResponse{
        Name: "create_ticket_long_running",
        ID:   funcCallID,
        Response: map[string]any{
            "status":    "approved",
            "ticket_id": ticketID,
        },
        WillContinue: &willContinue,
    }
    appResponseWithStatus := &genai.Content{
        Role:  string(genai.RoleUser),
        Parts: []*genai.Part{{FunctionResponse: ticketStatusResponse}},
    }
    runTurn(ctx, r, sess.Session.ID(), "Turn 2: App provides ticket status", appResponseWithStatus)
    fmt.Println("Long running function completed successfully.")
}

// printEventSummary logs text parts and function calls for each event.
func printEventSummary(event *session.Event, turnLabel string) {
    for _, part := range event.Content.Parts {
        if part.Text != "" {
            fmt.Printf("[%s][%s_TEXT]: %s\n", turnLabel, event.Author, part.Text)
        }
        if fc := part.FunctionCall; fc != nil {
            fmt.Printf("[%s][%s_CALL]: %s(%v) ID: %s\n", turnLabel, event.Author, fc.Name, fc.Args, fc.ID)
        }
    }
}
```

## AgentTool — Usage

Minimal snippet: wrap an agent with `agenttool.New` and pass it to the parent agent's tool list.

```go
agenttool.New(agent, &agenttool.Config{...})
```

## AgentTool — Full Example with `SkipSummarization`

A main agent wraps a summarizer agent via `agenttool.New` with `SkipSummarization: true`, then delegates a long-text summarization task.

```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/model/gemini"
    "google.golang.org/adk/tool"
    "google.golang.org/adk/tool/agenttool"
    "google.golang.org/genai"
)

// createSummarizerAgent creates an agent whose sole purpose is to summarize text.
func createSummarizerAgent(ctx context.Context) (agent.Agent, error) {
    model, err := gemini.NewModel(ctx, "gemini-2.5-flash", &genai.ClientConfig{})
    if err != nil {
        return nil, err
    }
    return llmagent.New(llmagent.Config{
        Name:        "SummarizerAgent",
        Model:       model,
        Instruction: "You are an expert at summarizing text. Take the user's input and provide a concise summary.",
        Description: "An agent that summarizes text.",
    })
}

// createMainAgent creates the primary agent that will use the summarizer agent as a tool.
func createMainAgent(ctx context.Context, tools ...tool.Tool) (agent.Agent, error) {
    model, err := gemini.NewModel(ctx, "gemini-2.5-flash", &genai.ClientConfig{})
    if err != nil {
        return nil, err
    }
    return llmagent.New(llmagent.Config{
        Name:  "MainAgent",
        Model: model,
        Instruction: "You are a helpful assistant. If you are asked to summarize a long text, use the 'summarize' tool. " +
            "After getting the summary, present it to the user by saying 'Here is a summary of the text:'.",
        Description: "The main agent that can delegate tasks.",
        Tools:       tools,
    })
}

func RunAgentAsToolSimulation() {
    ctx := context.Background()

    // 1. Create the Tool Agent (Summarizer)
    summarizerAgent, err := createSummarizerAgent(ctx)
    if err != nil {
        log.Fatalf("Failed to create summarizer agent: %v", err)
    }

    // 2. Wrap the Tool Agent in an AgentTool with SkipSummarization
    summarizeTool := agenttool.New(summarizerAgent, &agenttool.Config{
        SkipSummarization: true,
    })

    // 3. Create the Main Agent and provide it with the AgentTool
    mainAgent, err := createMainAgent(ctx, summarizeTool)
    if err != nil {
        log.Fatalf("Failed to create main agent: %v", err)
    }

    // 4. Run the main agent with a summarization request
    prompt := `Please summarize this text for me:
        Quantum computing represents a fundamentally different approach to computation,
        leveraging the bizarre principles of quantum mechanics to process information.`
    fmt.Printf("\nPrompt: %s\nResponse: ", prompt)
    callAgent(context.Background(), mainAgent, prompt)
    fmt.Println("\n---")
}
```
