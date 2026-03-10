# Multi-Agent Systems — TypeScript Examples

## 1.1. Agent Hierarchy (Parent agent, Sub Agents)

Defines a parent `LlmAgent` with two child agents passed via `subAgents`; the framework automatically sets `parentAgent` on each child.

```typescript
// Conceptual Example: Defining Hierarchy
import { LlmAgent, BaseAgent, InvocationContext } from '@google/adk';
import type { Event, createEventActions } from '@google/adk';

class TaskExecutorAgent extends BaseAgent {
  async *runAsyncImpl(context: InvocationContext): AsyncGenerator<Event, void, void> {
    yield {
      id: 'event-1',
      invocationId: context.invocationId,
      author: this.name,
      content: { parts: [{ text: 'Task completed!' }] },
      actions: createEventActions(),
      timestamp: Date.now(),
    };
  }
  async *runLiveImpl(context: InvocationContext): AsyncGenerator<Event, void, void> {
    this.runAsyncImpl(context);
  }
}

// Define individual agents
const greeter = new LlmAgent({name: 'Greeter', model: 'gemini-2.5-flash'});
const taskDoer = new TaskExecutorAgent({name: 'TaskExecutor'}); // Custom non-LLM agent

// Create parent agent and assign children via subAgents
const coordinator = new LlmAgent({
    name: 'Coordinator',
    model: 'gemini-2.5-flash',
    description: 'I coordinate greetings and tasks.',
    subAgents: [ // Assign subAgents here
        greeter,
        taskDoer
    ],
});

// Framework automatically sets:
// console.assert(greeter.parentAgent === coordinator);
// console.assert(taskDoer.parentAgent === coordinator);
```

## 1.2. Workflow Agents as Orchestrators

### SequentialAgent — outputKey pipeline chaining

Passes `outputKey: 'data'` on the first agent so its response is stored in `state['data']`, which the second agent reads via instruction template substitution.

```typescript
// Conceptual Example: Sequential Pipeline
import { SequentialAgent, LlmAgent } from '@google/adk';

const step1 = new LlmAgent({name: 'Step1_Fetch', outputKey: 'data'}); // Saves output to state['data']
const step2 = new LlmAgent({name: 'Step2_Process', instruction: 'Process data from {data}.'});

const pipeline = new SequentialAgent({name: 'MyPipeline', subAgents: [step1, step2]});
// When pipeline runs, Step2 can access the state['data'] set by Step1.
```

### ParallelAgent — shared session state with distinct output keys

Two sub-agents run concurrently and write to separate state keys; a downstream agent reads both after the parallel phase completes.

```typescript
// Conceptual Example: Parallel Execution
import { ParallelAgent, LlmAgent } from '@google/adk';

const fetchWeather = new LlmAgent({name: 'WeatherFetcher', outputKey: 'weather'});
const fetchNews = new LlmAgent({name: 'NewsFetcher', outputKey: 'news'});

const gatherer = new ParallelAgent({name: 'InfoGatherer', subAgents: [fetchWeather, fetchNews]});
// When gatherer runs, WeatherFetcher and NewsFetcher run concurrently.
// A subsequent agent could read state['weather'] and state['news'].
```

### LoopAgent — custom agent escalates when condition is met

A custom `BaseAgent` checks `ctx.session.state` each iteration and sets `escalate: isDone` to break the loop.

```typescript
// Conceptual Example: Loop with Condition
import { LoopAgent, LlmAgent, BaseAgent, InvocationContext } from '@google/adk';
import type { Event, createEventActions } from '@google/adk';

class CheckConditionAgent extends BaseAgent { // Custom agent to check state
    async *runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event> {
        const status = ctx.session.state['status'] || 'pending';
        const isDone = status === 'completed';
        yield createEvent({ author: 'check_condition', actions: createEventActions({ escalate: isDone }) });
    }
    async *runLiveImpl(ctx: InvocationContext): AsyncGenerator<Event> {
        // Not implemented.
    }
}

const processStep = new LlmAgent({name: 'ProcessingStep'});

const poller = new LoopAgent({
    name: 'StatusPoller',
    maxIterations: 10,
    subAgents: [processStep, new CheckConditionAgent({name: 'Checker'})]
});
// Executes processStep then Checker repeatedly until escalate or 10 iterations.
```

## 1.3. Interaction & Communication Mechanisms

### Shared Session State — outputKey chaining

`agentA` saves its response to `state['capital_city']` via `outputKey`; `agentB`'s instruction template reads it automatically.

```typescript
// Conceptual Example: Using outputKey and reading state
import { LlmAgent, SequentialAgent } from '@google/adk';

const agentA = new LlmAgent({name: 'AgentA', instruction: 'Find the capital of France.', outputKey: 'capital_city'});
const agentB = new LlmAgent({name: 'AgentB', instruction: 'Tell me about the city stored in {capital_city}.'});

const pipeline = new SequentialAgent({name: 'CityInfo', subAgents: [agentA, agentB]});
// AgentA saves "Paris" to state['capital_city']; AgentB reads it.
```

### LLM-Driven Delegation — transfer_to_agent routing

The coordinator's LLM emits a `transfer_to_agent` function call targeting `'Booker'` or `'Info'`; `AutoFlow` intercepts and routes execution.

```typescript
// Conceptual Setup: LLM Transfer
import { LlmAgent } from '@google/adk';

const bookingAgent = new LlmAgent({name: 'Booker', description: 'Handles flight and hotel bookings.'});
const infoAgent = new LlmAgent({name: 'Info', description: 'Provides general information and answers questions.'});

const coordinator = new LlmAgent({
    name: 'Coordinator',
    model: 'gemini-2.5-flash',
    instruction: 'You are an assistant. Delegate booking tasks to Booker and info requests to Info.',
    description: 'Main coordinator.',
    subAgents: [bookingAgent, infoAgent]
});
// "Book a flight" -> transfer_to_agent({agent_name: 'Booker'})
// ADK framework routes execution to bookingAgent.
```

### AgentTool — wrapping an agent as a callable tool

`AgentTool` wraps a custom `BaseAgent` so the parent LLM can invoke it like a regular tool; the tool captures the sub-agent's final response and returns it as the tool result.

```typescript
// Conceptual Setup: Agent as a Tool
import { LlmAgent, BaseAgent, AgentTool, InvocationContext } from '@google/adk';
import type { Part, Event } from '@google/genai';

class ImageGeneratorAgent extends BaseAgent {
    constructor() {
        super({name: 'ImageGen', description: 'Generates an image based on a prompt.'});
    }
    async *runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event> {
        const prompt = ctx.session.state['image_prompt'] || 'default prompt';
        const imageBytes = new Uint8Array(); // placeholder
        const imagePart: Part = {inlineData: {data: Buffer.from(imageBytes).toString('base64'), mimeType: 'image/png'}};
        yield createEvent({content: {parts: [imagePart]}});
    }
    async *runLiveImpl(ctx: InvocationContext): AsyncGenerator<Event, void, void> {
        // Not implemented.
    }
}

const imageAgent = new ImageGeneratorAgent();
const imageTool = new AgentTool({agent: imageAgent}); // Wrap the agent

const artistAgent = new LlmAgent({
    name: 'Artist',
    model: 'gemini-2.5-flash',
    instruction: 'Create a prompt and use the ImageGen tool to generate the image.',
    tools: [imageTool]
});
// Artist LLM calls ImageGen tool; framework runs ImageGeneratorAgent and returns result.
```

## 2. Common Multi-Agent Patterns

### Coordinator/Dispatcher Pattern

LLM transfer routes each user request to a specialist sub-agent by description matching.

```typescript
// Conceptual Code: Coordinator using LLM Transfer
import { LlmAgent } from '@google/adk';

const billingAgent = new LlmAgent({name: 'Billing', description: 'Handles billing inquiries.'});
const supportAgent = new LlmAgent({name: 'Support', description: 'Handles technical support requests.'});

const coordinator = new LlmAgent({
    name: 'HelpDeskCoordinator',
    model: 'gemini-2.5-flash',
    instruction: 'Route user requests: Use Billing agent for payment issues, Support agent for technical problems.',
    description: 'Main help desk router.',
    subAgents: [billingAgent, supportAgent]
});
// "My payment failed" -> transfer_to_agent({agent_name: 'Billing'})
// "I can't log in"   -> transfer_to_agent({agent_name: 'Support'})
```

### Sequential Pipeline Pattern

Three-stage pipeline chains `outputKey` values so each agent reads the previous agent's result from state.

```typescript
// Conceptual Code: Sequential Data Pipeline
import { SequentialAgent, LlmAgent } from '@google/adk';

const validator = new LlmAgent({name: 'ValidateInput', instruction: 'Validate the input.', outputKey: 'validation_status'});
const processor = new LlmAgent({name: 'ProcessData', instruction: 'Process data if {validation_status} is "valid".', outputKey: 'result'});
const reporter  = new LlmAgent({name: 'ReportResult', instruction: 'Report the result from {result}.'});

const dataPipeline = new SequentialAgent({name: 'DataPipeline', subAgents: [validator, processor, reporter]});
// validator -> state['validation_status'] -> processor -> state['result'] -> reporter
```

### Parallel Fan-Out/Gather Pattern

`ParallelAgent` fans out to two fetchers simultaneously; a downstream synthesizer inside a `SequentialAgent` gathers both state keys.

```typescript
// Conceptual Code: Parallel Information Gathering
import { SequentialAgent, ParallelAgent, LlmAgent } from '@google/adk';

const fetchApi1 = new LlmAgent({name: 'API1Fetcher', instruction: 'Fetch data from API 1.', outputKey: 'api1_data'});
const fetchApi2 = new LlmAgent({name: 'API2Fetcher', instruction: 'Fetch data from API 2.', outputKey: 'api2_data'});

const gatherConcurrently = new ParallelAgent({name: 'ConcurrentFetch', subAgents: [fetchApi1, fetchApi2]});
const synthesizer = new LlmAgent({name: 'Synthesizer', instruction: 'Combine results from {api1_data} and {api2_data}.'});

const overallWorkflow = new SequentialAgent({
    name: 'FetchAndSynthesize',
    subAgents: [gatherConcurrently, synthesizer]
});
// Fetchers run concurrently; synthesizer reads both state keys afterwards.
```

### Hierarchical Task Decomposition

A high-level `ReportWriter` wraps a mid-level `ResearchAssistant` as an `AgentTool`, which itself wraps `WebSearch` and `Summarizer` — three-level hierarchy via `AgentTool`.

```typescript
// Conceptual Code: Hierarchical Research Task
import { LlmAgent, AgentTool } from '@google/adk';

const webSearcher = new LlmAgent({name: 'WebSearch', description: 'Performs web searches for facts.'});
const summarizer  = new LlmAgent({name: 'Summarizer', description: 'Summarizes text.'});

const researchAssistant = new LlmAgent({
    name: 'ResearchAssistant',
    model: 'gemini-2.5-flash',
    description: 'Finds and summarizes information on a topic.',
    tools: [new AgentTool({agent: webSearcher}), new AgentTool({agent: summarizer})]
});

const reportWriter = new LlmAgent({
    name: 'ReportWriter',
    model: 'gemini-2.5-flash',
    instruction: 'Write a report on topic X. Use the ResearchAssistant to gather information.',
    tools: [new AgentTool({agent: researchAssistant})]
});
// ReportWriter -> ResearchAssistant -> WebSearch / Summarizer; results flow back up.
```

### Review/Critique Pattern (Generator-Critic)

`DraftWriter` saves its output to `state['draft_text']` via `outputKey`; `FactChecker` reads that key and saves its verdict to `state['review_status']`.

```typescript
// Conceptual Code: Generator-Critic
import { SequentialAgent, LlmAgent } from '@google/adk';

const generator = new LlmAgent({
    name: 'DraftWriter',
    instruction: 'Write a short paragraph about subject X.',
    outputKey: 'draft_text'
});

const reviewer = new LlmAgent({
    name: 'FactChecker',
    instruction: 'Review the text in {draft_text} for factual accuracy. Output "valid" or "invalid" with reasons.',
    outputKey: 'review_status'
});

const reviewPipeline = new SequentialAgent({name: 'WriteAndReview', subAgents: [generator, reviewer]});
// generator -> state['draft_text'] -> reviewer -> state['review_status']
```

### Iterative Refinement Pattern

`LoopAgent` cycles through a refiner, quality checker, and custom escalator; `CheckStatusAndEscalate` sets `escalate: true` when `state['quality_status'] === 'pass'`.

```typescript
// Conceptual Code: Iterative Code Refinement
import { LoopAgent, LlmAgent, BaseAgent, InvocationContext } from '@google/adk';
import type { Event, createEvent, createEventActions } from '@google/adk';

const codeRefiner = new LlmAgent({
    name: 'CodeRefiner',
    instruction: 'Read state["current_code"] and state["requirements"]. Refine code. Save to state["current_code"].',
    outputKey: 'current_code'
});

const qualityChecker = new LlmAgent({
    name: 'QualityChecker',
    instruction: 'Evaluate state["current_code"] against state["requirements"]. Output "pass" or "fail".',
    outputKey: 'quality_status'
});

class CheckStatusAndEscalate extends BaseAgent {
    async *runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event> {
        const shouldStop = ctx.session.state['quality_status'] === 'pass';
        if (shouldStop) {
            yield createEvent({ author: 'StopChecker', actions: createEventActions({ escalate: true }) });
        }
    }
    async *runLiveImpl(ctx: InvocationContext): AsyncGenerator<Event> {
        yield createEvent({ author: 'StopChecker' });
    }
}

const refinementLoop = new LoopAgent({
    name: 'CodeRefinementLoop',
    maxIterations: 5,
    subAgents: [codeRefiner, qualityChecker, new CheckStatusAndEscalate({name: 'StopChecker'})]
});
// Refiner -> Checker -> StopChecker each iteration; stops on 'pass' or 5 iterations.
```

### Human-in-the-Loop Pattern

A `FunctionTool` wrapping an external approval call is given to `RequestHumanApproval`; it blocks until a human responds, then returns the decision into the pipeline.

```typescript
// Conceptual Code: Using a Tool for Human Approval
import { LlmAgent, SequentialAgent, FunctionTool } from '@google/adk';
import { z } from 'zod';

// externalApprovalTool sends request to human review system and returns decision
const approvalTool = new FunctionTool({
  name: 'external_approval_tool',
  description: 'Sends a request for human approval and waits for response.',
  parameters: z.object({ amount: z.number(), reason: z.string() }),
  execute: async (params) => {
    // ... call external review system, await human response ...
    return {decision: 'approved'}; // or 'rejected'
  },
});

const prepareRequest = new LlmAgent({
    name: 'PrepareApproval',
    instruction: 'Prepare approval request details. Store amount and reason in state.',
});

const requestApproval = new LlmAgent({
    name: 'RequestHumanApproval',
    instruction: 'Use external_approval_tool with amount from state["approval_amount"] and reason from state["approval_reason"].',
    tools: [approvalTool],
    outputKey: 'human_decision'
});

const processDecision = new LlmAgent({
    name: 'ProcessDecision',
    instruction: 'Check {human_decision}. If "approved", proceed. If "rejected", inform user.'
});

const approvalWorkflow = new SequentialAgent({
    name: 'HumanApprovalWorkflow',
    subAgents: [prepareRequest, requestApproval, processDecision]
});
```

### Human in the Loop with Policy

A `SecurityPlugin` with a custom `BasePolicyEngine` intercepts every tool call; returning `PolicyOutcome.CONFIRM` pauses execution and requests explicit user confirmation before proceeding.

```typescript
// Conceptual Code: PolicyEngine-based Human Confirmation (TypeScript only)
import { LlmAgent, InMemoryRunner, SecurityPlugin, BasePolicyEngine, PolicyOutcome } from '@google/adk';
import type { ToolCallPolicyContext, PolicyCheckResult } from '@google/adk';

const rootAgent = new LlmAgent({
  name: 'weather_time_agent',
  model: 'gemini-2.5-flash',
  description: 'Agent to answer questions about the time and weather in a city.',
  instruction: 'You are a helpful agent who can answer user questions about the time and weather in a city.',
  tools: [getWeatherTool],
});

class CustomPolicyEngine implements BasePolicyEngine {
  async evaluate(_context: ToolCallPolicyContext): Promise<PolicyCheckResult> {
    return Promise.resolve({
      outcome: PolicyOutcome.CONFIRM,
      reason: 'Needs confirmation for tool call',
    });
  }
}

const runner = new InMemoryRunner({
    agent: rootAgent,
    appName,
    plugins: [new SecurityPlugin({policyEngine: new CustomPolicyEngine()})]
});
// SecurityPlugin intercepts every tool call; CONFIRM outcome pauses execution
// and emits a confirmation request to the application layer.
```
