# Multi-Agent Systems — Go Examples

## 1.1. Agent Hierarchy (Parent agent, Sub Agents)

Defines a parent `llmagent` with two child agents passed via `SubAgents`; the framework automatically sets the parent reference on each child.

```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
)

// Conceptual Example: Defining Hierarchy
// Define individual agents
greeter, _ := llmagent.New(llmagent.Config{Name: "Greeter", Model: m})
taskDoer, _ := agent.New(agent.Config{Name: "TaskExecutor"}) // Custom non-LLM agent

// Create parent agent and assign children via SubAgents
coordinator, _ := llmagent.New(llmagent.Config{
    Name:        "Coordinator",
    Model:       m,
    Description: "I coordinate greetings and tasks.",
    SubAgents:   []agent.Agent{greeter, taskDoer}, // Assign SubAgents here
})
```

## 1.2. Workflow Agents as Orchestrators

### SequentialAgent — OutputKey pipeline chaining

Passes `OutputKey: "data"` on the first agent so its response is stored in `state["data"]`, which the second agent reads via instruction template substitution.

```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/sequentialagent"
)

// Conceptual Example: Sequential Pipeline
step1, _ := llmagent.New(llmagent.Config{Name: "Step1_Fetch", OutputKey: "data", Model: m}) // Saves output to state["data"]
step2, _ := llmagent.New(llmagent.Config{Name: "Step2_Process", Instruction: "Process data from {data}.", Model: m})

pipeline, _ := sequentialagent.New(sequentialagent.Config{
    AgentConfig: agent.Config{Name: "MyPipeline", SubAgents: []agent.Agent{step1, step2}},
})
// When pipeline runs, Step2 can access the state["data"] set by Step1.
```

### ParallelAgent — shared session state with distinct output keys

Two sub-agents run concurrently and write to separate state keys; a downstream agent reads both after the parallel phase completes.

```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/parallelagent"
)

// Conceptual Example: Parallel Execution
fetchWeather, _ := llmagent.New(llmagent.Config{Name: "WeatherFetcher", OutputKey: "weather", Model: m})
fetchNews, _ := llmagent.New(llmagent.Config{Name: "NewsFetcher", OutputKey: "news", Model: m})

gatherer, _ := parallelagent.New(parallelagent.Config{
    AgentConfig: agent.Config{Name: "InfoGatherer", SubAgents: []agent.Agent{fetchWeather, fetchNews}},
})
// When gatherer runs, WeatherFetcher and NewsFetcher run concurrently.
// A subsequent agent could read state["weather"] and state["news"].
```

### LoopAgent — custom agent escalates when condition is met

A custom agent's `Run` func checks `state["status"]` each iteration and sets `Escalate: isDone` in `EventActions` to break the loop.

```go
import (
    "iter"
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/loopagent"
    "google.golang.org/adk/session"
)

// Conceptual Example: Loop with Condition
// Custom agent to check state
checkCondition, _ := agent.New(agent.Config{
    Name: "Checker",
    Run: func(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
        return func(yield func(*session.Event, error) bool) {
            status, err := ctx.Session().State().Get("status")
            if err != nil {
                status = "pending"
            }
            isDone := status == "completed"
            yield(&session.Event{Author: "Checker", Actions: session.EventActions{Escalate: isDone}}, nil)
        }
    },
})

processStep, _ := llmagent.New(llmagent.Config{Name: "ProcessingStep", Model: m})

poller, _ := loopagent.New(loopagent.Config{
    MaxIterations: 10,
    AgentConfig:   agent.Config{Name: "StatusPoller", SubAgents: []agent.Agent{processStep, checkCondition}},
})
// Executes processStep then Checker repeatedly until Escalate=true or 10 iterations.
```

## 1.3. Interaction & Communication Mechanisms

### Shared Session State — OutputKey chaining

`agentA` saves its response to `state["capital_city"]` via `OutputKey`; `agentB`'s instruction template reads it automatically.

```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/sequentialagent"
)

// Conceptual Example: Using OutputKey and reading state
agentA, _ := llmagent.New(llmagent.Config{Name: "AgentA", Instruction: "Find the capital of France.", OutputKey: "capital_city", Model: m})
agentB, _ := llmagent.New(llmagent.Config{Name: "AgentB", Instruction: "Tell me about the city stored in {capital_city}.", Model: m})

pipeline2, _ := sequentialagent.New(sequentialagent.Config{
    AgentConfig: agent.Config{Name: "CityInfo", SubAgents: []agent.Agent{agentA, agentB}},
})
// AgentA saves "Paris" to state["capital_city"]; AgentB reads it.
```

### LLM-Driven Delegation — transfer_to_agent routing

The coordinator's LLM emits `transfer_to_agent(agent_name='Booker')` or `transfer_to_agent(agent_name='Info')`; `AutoFlow` intercepts and routes execution.

```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
)

// Conceptual Setup: LLM Transfer
bookingAgent, _ := llmagent.New(llmagent.Config{Name: "Booker", Description: "Handles flight and hotel bookings.", Model: m})
infoAgent, _ := llmagent.New(llmagent.Config{Name: "Info", Description: "Provides general information and answers questions.", Model: m})

coordinator, _ = llmagent.New(llmagent.Config{
    Name:        "Coordinator",
    Model:       m,
    Instruction: "You are an assistant. Delegate booking tasks to Booker and info requests to Info.",
    Description: "Main coordinator.",
    SubAgents:   []agent.Agent{bookingAgent, infoAgent},
})
// "Book a flight" -> FunctionCall{Name: "transfer_to_agent", Args: {"agent_name": "Booker"}}
// ADK framework routes execution to bookingAgent.
```

### AgentTool — wrapping an agent as a callable tool

`agenttool.New` wraps a custom agent so the parent LLM can invoke it like a regular tool; the tool captures the sub-agent's final response and returns it as the tool result.

```go
import (
    "fmt"
    "iter"
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/model"
    "google.golang.org/adk/session"
    "google.golang.org/adk/tool"
    "google.golang.org/adk/tool/agenttool"
    "google.golang.org/genai"
)

// Conceptual Setup: Agent as a Tool
imageAgent, _ := agent.New(agent.Config{
    Name:        "ImageGen",
    Description: "Generates an image based on a prompt.",
    Run: func(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
        return func(yield func(*session.Event, error) bool) {
            prompt, _ := ctx.Session().State().Get("image_prompt")
            fmt.Printf("Generating image for prompt: %v\n", prompt)
            imageBytes := []byte("...") // Simulate image bytes
            yield(&session.Event{
                Author: "ImageGen",
                LLMResponse: model.LLMResponse{
                    Content: &genai.Content{
                        Parts: []*genai.Part{genai.NewPartFromBytes(imageBytes, "image/png")},
                    },
                },
            }, nil)
        }
    },
})

// Wrap the agent as a tool
imageTool := agenttool.New(imageAgent, nil)

// Parent agent uses the AgentTool
artistAgent, _ := llmagent.New(llmagent.Config{
    Name:        "Artist",
    Model:       m,
    Instruction: "Create a prompt and use the ImageGen tool to generate the image.",
    Tools:       []tool.Tool{imageTool},
})
// Artist LLM calls ImageGen tool; framework runs imageAgent and returns result.
```

## 2. Common Multi-Agent Patterns

### Coordinator/Dispatcher Pattern

LLM transfer routes each user request to a specialist sub-agent by description matching.

```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
)

// Conceptual Code: Coordinator using LLM Transfer
billingAgent, _ := llmagent.New(llmagent.Config{Name: "Billing", Description: "Handles billing inquiries.", Model: m})
supportAgent, _ := llmagent.New(llmagent.Config{Name: "Support", Description: "Handles technical support requests.", Model: m})

coordinator, _ := llmagent.New(llmagent.Config{
    Name:        "HelpDeskCoordinator",
    Model:       m,
    Instruction: "Route user requests: Use Billing agent for payment issues, Support agent for technical problems.",
    Description: "Main help desk router.",
    SubAgents:   []agent.Agent{billingAgent, supportAgent},
})
// "My payment failed" -> transfer_to_agent(agent_name='Billing')
// "I can't log in"   -> transfer_to_agent(agent_name='Support')
```

### Sequential Pipeline Pattern

Three-stage pipeline chains `OutputKey` values so each agent reads the previous agent's result from state.

```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/sequentialagent"
)

// Conceptual Code: Sequential Data Pipeline
validator, _ := llmagent.New(llmagent.Config{Name: "ValidateInput", Instruction: "Validate the input.", OutputKey: "validation_status", Model: m})
processor, _ := llmagent.New(llmagent.Config{Name: "ProcessData", Instruction: "Process data if {validation_status} is 'valid'.", OutputKey: "result", Model: m})
reporter, _ := llmagent.New(llmagent.Config{Name: "ReportResult", Instruction: "Report the result from {result}.", Model: m})

dataPipeline, _ := sequentialagent.New(sequentialagent.Config{
    AgentConfig: agent.Config{Name: "DataPipeline", SubAgents: []agent.Agent{validator, processor, reporter}},
})
// validator -> state["validation_status"] -> processor -> state["result"] -> reporter
```

### Parallel Fan-Out/Gather Pattern

`ParallelAgent` fans out to two fetchers simultaneously; a downstream synthesizer inside a `SequentialAgent` gathers both state keys.

```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/parallelagent"
    "google.golang.org/adk/agent/workflowagents/sequentialagent"
)

// Conceptual Code: Parallel Information Gathering
fetchAPI1, _ := llmagent.New(llmagent.Config{Name: "API1Fetcher", Instruction: "Fetch data from API 1.", OutputKey: "api1_data", Model: m})
fetchAPI2, _ := llmagent.New(llmagent.Config{Name: "API2Fetcher", Instruction: "Fetch data from API 2.", OutputKey: "api2_data", Model: m})

gatherConcurrently, _ := parallelagent.New(parallelagent.Config{
    AgentConfig: agent.Config{Name: "ConcurrentFetch", SubAgents: []agent.Agent{fetchAPI1, fetchAPI2}},
})

synthesizer, _ := llmagent.New(llmagent.Config{Name: "Synthesizer", Instruction: "Combine results from {api1_data} and {api2_data}.", Model: m})

overallWorkflow, _ := sequentialagent.New(sequentialagent.Config{
    AgentConfig: agent.Config{Name: "FetchAndSynthesize", SubAgents: []agent.Agent{gatherConcurrently, synthesizer}},
})
// Fetchers run concurrently; synthesizer reads both state keys afterwards.
```

### Hierarchical Task Decomposition

A high-level `reportWriter` wraps a mid-level `researchAssistant` via `agenttool.New`, which itself wraps `webSearcher` and `summarizer` — three-level hierarchy.

```go
import (
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/tool"
    "google.golang.org/adk/tool/agenttool"
)

// Conceptual Code: Hierarchical Research Task
// Low-level tool-like agents
webSearcher, _ := llmagent.New(llmagent.Config{Name: "WebSearch", Description: "Performs web searches for facts.", Model: m})
summarizer, _ := llmagent.New(llmagent.Config{Name: "Summarizer", Description: "Summarizes text.", Model: m})

// Mid-level agent combining tools
webSearcherTool := agenttool.New(webSearcher, nil)
summarizerTool := agenttool.New(summarizer, nil)
researchAssistant, _ := llmagent.New(llmagent.Config{
    Name:        "ResearchAssistant",
    Model:       m,
    Description: "Finds and summarizes information on a topic.",
    Tools:       []tool.Tool{webSearcherTool, summarizerTool},
})

// High-level agent delegating research
researchAssistantTool := agenttool.New(researchAssistant, nil)
reportWriter, _ := llmagent.New(llmagent.Config{
    Name:        "ReportWriter",
    Model:       m,
    Instruction: "Write a report on topic X. Use the ResearchAssistant to gather information.",
    Tools:       []tool.Tool{researchAssistantTool},
})
// ReportWriter -> ResearchAssistant -> WebSearch / Summarizer; results flow back up.
```

### Review/Critique Pattern (Generator-Critic)

`DraftWriter` saves its output to `state["draft_text"]` via `OutputKey`; `FactChecker` reads that key and saves its verdict to `state["review_status"]`.

```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/sequentialagent"
)

// Conceptual Code: Generator-Critic
generator, _ := llmagent.New(llmagent.Config{
    Name:        "DraftWriter",
    Instruction: "Write a short paragraph about subject X.",
    OutputKey:   "draft_text",
    Model:       m,
})

reviewer, _ := llmagent.New(llmagent.Config{
    Name:        "FactChecker",
    Instruction: "Review the text in {draft_text} for factual accuracy. Output 'valid' or 'invalid' with reasons.",
    OutputKey:   "review_status",
    Model:       m,
})

reviewPipeline, _ := sequentialagent.New(sequentialagent.Config{
    AgentConfig: agent.Config{Name: "WriteAndReview", SubAgents: []agent.Agent{generator, reviewer}},
})
// generator -> state["draft_text"] -> reviewer -> state["review_status"]
```

### Iterative Refinement Pattern

`LoopAgent` cycles through a refiner, quality checker, and custom escalator agent; `StopChecker` sets `Escalate: true` when `state["quality_status"] == "pass"`.

```go
import (
    "iter"
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/loopagent"
    "google.golang.org/adk/session"
)

// Conceptual Code: Iterative Code Refinement
codeRefiner, _ := llmagent.New(llmagent.Config{
    Name:        "CodeRefiner",
    Instruction: "Read state['current_code'] (if exists) and state['requirements']. Generate/refine Go code to meet requirements.",
    OutputKey:   "current_code",
    Model:       m,
})

qualityChecker, _ := llmagent.New(llmagent.Config{
    Name:        "QualityChecker",
    Instruction: "Evaluate the code in state['current_code'] against state['requirements']. Output 'pass' or 'fail'.",
    OutputKey:   "quality_status",
    Model:       m,
})

// Custom agent that escalates when quality_status == "pass"
checkStatusAndEscalate, _ := agent.New(agent.Config{
    Name: "StopChecker",
    Run: func(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
        return func(yield func(*session.Event, error) bool) {
            status, _ := ctx.Session().State().Get("quality_status")
            shouldStop := status == "pass"
            yield(&session.Event{Author: "StopChecker", Actions: session.EventActions{Escalate: shouldStop}}, nil)
        }
    },
})

refinementLoop, _ := loopagent.New(loopagent.Config{
    MaxIterations: 5,
    AgentConfig:   agent.Config{Name: "CodeRefinementLoop", SubAgents: []agent.Agent{codeRefiner, qualityChecker, checkStatusAndEscalate}},
})
// Refiner -> Checker -> StopChecker each iteration; stops on 'pass' or 5 iterations.
```

### Human-in-the-Loop Pattern

A `functiontool` wrapping an external approval call is given to `requestApproval`; it blocks until a human responds, then returns the decision into the sequential pipeline.

```go
import (
    "google.golang.org/adk/agent"
    "google.golang.org/adk/agent/llmagent"
    "google.golang.org/adk/agent/workflowagents/sequentialagent"
    "google.golang.org/adk/tool"
)

// Conceptual Code: Using a Tool for Human Approval
// externalApprovalTool sends request to human review system and returns decision
type externalApprovalToolArgs struct {
    Amount float64 `json:"amount" jsonschema:"The amount for which approval is requested."`
    Reason string  `json:"reason" jsonschema:"The reason for the approval request."`
}
var externalApprovalTool func(tool.Context, externalApprovalToolArgs) (string, error)
approvalTool, _ := functiontool.New(
    functiontool.Config{
        Name:        "external_approval_tool",
        Description: "Sends a request for human approval.",
    },
    externalApprovalTool,
)

prepareRequest, _ := llmagent.New(llmagent.Config{
    Name:        "PrepareApproval",
    Instruction: "Prepare the approval request details based on user input. Store amount and reason in state.",
    Model:       m,
})

requestApproval, _ := llmagent.New(llmagent.Config{
    Name:        "RequestHumanApproval",
    Instruction: "Use the external_approval_tool with amount from state['approval_amount'] and reason from state['approval_reason'].",
    Tools:       []tool.Tool{approvalTool},
    OutputKey:   "human_decision",
    Model:       m,
})

processDecision, _ := llmagent.New(llmagent.Config{
    Name:        "ProcessDecision",
    Instruction: "Check {human_decision}. If 'approved', proceed. If 'rejected', inform user.",
    Model:       m,
})

approvalWorkflow, _ := sequentialagent.New(sequentialagent.Config{
    AgentConfig: agent.Config{Name: "HumanApprovalWorkflow", SubAgents: []agent.Agent{prepareRequest, requestApproval, processDecision}},
})
```
