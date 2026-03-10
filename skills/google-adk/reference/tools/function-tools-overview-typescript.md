# Function Tools — TypeScript Examples

## Function Tool Example — Stock Price Agent

Full working example: a `FunctionTool` built with a Zod schema, executed via `InMemoryRunner`. Returns a mock price object.

```typescript
import {Content, createUserContent} from '@google/genai';
import { stringifyContent, FunctionTool, InMemoryRunner, LlmAgent } from '@google/adk';
import {z} from 'zod';

async function getStockPrice({ticker}: {ticker: string}): Promise<Record<string, unknown>> {
  console.log(`Getting stock price for ${ticker}`);
  const price = (Math.random() * 1000).toFixed(2);
  return {price: `$${price}`};
}

async function main() {
  const getStockPriceSchema = z.object({
    ticker: z.string().describe('The stock ticker symbol to look up.'),
  });

  // Construct a FunctionTool wrapping the getStockPrice function and Zod schema
  const stockPriceTool = new FunctionTool({
    name: 'getStockPrice',
    description: 'Gets the current price of a stock.',
    parameters: getStockPriceSchema,
    execute: getStockPrice,
  });

  const stockAgent = new LlmAgent({
    name: 'stock_agent',
    model: 'gemini-2.5-flash',
    instruction: 'You can get the stock price of a company.',
    tools: [stockPriceTool],
  });

  const runner = new InMemoryRunner({agent: stockAgent});
  const session = await runner.sessionService.createSession({
    appName: runner.appName,
    userId: 'test-user',
  });

  const userContent: Content = createUserContent('What is the stock price of GOOG?');
  const response = [];
  for await (const event of runner.runAsync({
    userId: session.userId,
    sessionId: session.id,
    newMessage: userContent,
  })) {
    response.push(event);
  }

  const finalResponse = response[response.length - 1];
  if (finalResponse?.content?.parts?.length) {
    console.log(stringifyContent(finalResponse));
  }
}

main();
```

## LongRunningFunctionTool — Creating the Tool

Instantiate `LongRunningFunctionTool` with a Zod schema; the framework pauses agent execution after the initial response and waits for a client-provided `FunctionResponse`.

```typescript
import { LongRunningFunctionTool } from '@google/adk';
import {z} from 'zod';

function askForApproval(args: {purpose: string; amount: number}) {
  // Creates a ticket and notifies the approver; returns initial pending status
  return {
    status: "pending",
    approver: "Sean Zhou",
    purpose: args.purpose,
    amount: args.amount,
    "ticket-id": "approval-ticket-1",
  };
}

// Wrap with LongRunningFunctionTool so the agent runner pauses after invocation
const longRunningTool = new LongRunningFunctionTool({
  name: "ask_for_approval",
  description: "Ask for approval for the reimbursement.",
  parameters: z.object({
    purpose: z.string().describe("The purpose of the reimbursement."),
    amount: z.number().describe("The amount to reimburse."),
  }),
  execute: askForApproval,
});
```

## LongRunningFunctionTool — Intermediate / Final Result Updates (Complete Example)

Full reimbursement workflow: the client captures the long-running function call ID from the first `runAsync` loop, then sends an approved `FunctionResponse` in a second loop.

```typescript
import {
  LlmAgent, Runner, FunctionTool, LongRunningFunctionTool,
  InMemorySessionService, Event, stringifyContent
} from '@google/adk';
import {z} from "zod";
import {Content, FunctionCall, FunctionResponse, createUserContent} from "@google/genai";

function askForApproval(args: {purpose: string; amount: number}) {
  return {
    status: "pending",
    approver: "Sean Zhou",
    purpose: args.purpose,
    amount: args.amount,
    "ticket-id": "approval-ticket-1",
  };
}

const longRunningTool = new LongRunningFunctionTool({
  name: "ask_for_approval",
  description: "Ask for approval for the reimbursement.",
  parameters: z.object({
    purpose: z.string().describe("The purpose of the reimbursement."),
    amount: z.number().describe("The amount to reimburse."),
  }),
  execute: askForApproval,
});

function reimburse(args: {purpose: string; amount: number}) {
  return {status: "ok"};
}

const reimburseTool = new FunctionTool({
  name: "reimburse",
  description: "Reimburse the amount of money to the employee.",
  parameters: z.object({
    purpose: z.string().describe("The purpose of the reimbursement."),
    amount: z.number().describe("The amount to reimburse."),
  }),
  execute: reimburse,
});

const reimbursementAgent = new LlmAgent({
  model: "gemini-2.5-flash",
  name: "reimbursement_agent",
  instruction: `You are an agent whose job is to handle the reimbursement process for
      the employees. If the amount is less than $100, you will automatically
      approve the reimbursement. If the amount is greater than $100, you will
      ask for approval from the manager. If the manager approves, call reimburse().
      If the manager rejects, inform the employee of the rejection.`,
  tools: [reimburseTool, longRunningTool],
});

const APP_NAME = "human_in_the_loop";
const USER_ID = "1234";
const SESSION_ID = "session1234";

async function setupSessionAndRunner() {
  const sessionService = new InMemorySessionService();
  const session = await sessionService.createSession({
    appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID,
  });
  const runner = new Runner({
    agent: reimbursementAgent, appName: APP_NAME, sessionService,
  });
  return {session, runner};
}

// Helper: extract the long-running function call from an event
function getLongRunningFunctionCall(event: Event): FunctionCall | undefined {
  if (!event.longRunningToolIds || !event.content?.parts?.length) return;
  for (const part of event.content.parts) {
    if (part?.functionCall?.id &&
        event.longRunningToolIds.includes(part.functionCall.id)) {
      return part.functionCall;
    }
  }
}

// Helper: find the function response matching a given call ID
function getFunctionResponse(event: Event, functionCallId: string): FunctionResponse | undefined {
  if (!event.content?.parts?.length) return;
  for (const part of event.content.parts) {
    if (part?.functionResponse?.id === functionCallId) {
      return part.functionResponse;
    }
  }
}

async function callAgentAsync(query: string) {
  let longRunningFunctionCall: FunctionCall | undefined;
  let longRunningFunctionResponse: FunctionResponse | undefined;
  const {session, runner} = await setupSessionAndRunner();

  console.log("\nRunning agent...");

  // Turn 1: initial agent run — capture the long-running call ID
  for await (const event of runner.runAsync({
    sessionId: session.id, userId: USER_ID,
    newMessage: createUserContent(query),
  })) {
    if (!longRunningFunctionCall) {
      longRunningFunctionCall = getLongRunningFunctionCall(event);
    } else {
      const potential = getFunctionResponse(event, longRunningFunctionCall.id!);
      if (potential) longRunningFunctionResponse = potential;
    }
    const text = stringifyContent(event);
    if (text) console.log(`[${event.author}]: ${text}`);
  }

  // Turn 2: send the approved status back as a FunctionResponse
  if (longRunningFunctionResponse) {
    const updatedResponse = JSON.parse(JSON.stringify(longRunningFunctionResponse));
    updatedResponse.response = {status: "approved"};
    for await (const event of runner.runAsync({
      sessionId: session.id, userId: USER_ID,
      newMessage: createUserContent(JSON.stringify({functionResponse: updatedResponse})),
    })) {
      const text = stringifyContent(event);
      if (text) console.log(`[${event.author}]: ${text}`);
    }
  }
}

async function main() {
  await callAgentAsync("Please reimburse 50$ for meals");   // auto-approved
  await callAgentAsync("Please reimburse 200$ for meals");  // requires approval
}

main();
```

## AgentTool — Usage

Minimal snippet: wrap `agentB` in `AgentTool` and pass it to the parent agent's tool list.

```typescript
tools: [new AgentTool({agent: agentB})]
```

## AgentTool — Full Example with `skipSummarization`

A main agent delegates summarization to `summary_agent` via `AgentTool({skipSummarization: true})`, bypassing a second LLM pass on the result.

```typescript
import { AgentTool, InMemoryRunner, LlmAgent } from '@google/adk';
import {Part, createUserContent} from '@google/genai';

async function main() {
  const summaryAgent = new LlmAgent({
    name: 'summary_agent',
    model: 'gemini-2.5-flash',
    description: 'Agent to summarize text',
    instruction: 'You are an expert summarizer. Please read the following text and provide a concise summary.',
  });

  // skipSummarization: true passes the sub-agent's response back to the user unmodified
  const mainAgent = new LlmAgent({
    name: 'main_agent',
    model: 'gemini-2.5-flash',
    instruction:
      "You are a helpful assistant. When the user provides a text, use the 'summary_agent' tool to generate a summary. Always forward the user's message exactly as received to the tool, without modifying it yourself.",
    tools: [new AgentTool({agent: summaryAgent, skipSummarization: true})],
  });

  const appName = 'agent-as-a-tool-app';
  const runner = new InMemoryRunner({agent: mainAgent, appName});

  await runner.sessionService.createSession({appName, userId: 'user1', sessionId: 'session1'});

  const longText = `Quantum computing represents a fundamentally different approach to computation,
leveraging the bizarre principles of quantum mechanics to process information.`;

  const events = runner.runAsync({
    userId: 'user1', sessionId: 'session1',
    newMessage: createUserContent(longText),
  });

  console.log('Agent Response:');
  for await (const event of events) {
    if (event.content?.parts?.length) {
      const responsePart = event.content.parts.find((p: Part) => p.functionResponse);
      if (responsePart?.functionResponse) {
        console.log(responsePart.functionResponse.response);
      }
    }
  }
}

main();
```
