# Callback Types — TypeScript Examples

## before_agent_callback

Checks `skip_llm_agent` in session state. Returns `Content` to skip the agent, or `undefined` to proceed.

```typescript
import { LlmAgent, InMemoryRunner, Context, isFinalResponse } from '@google/adk';
import { Content, createUserContent } from "@google/genai";

const MODEL_NAME = "gemini-2.5-flash";
const APP_NAME = "before_agent_callback_app";
const USER_ID = "test_user_before_agent";
const SESSION_ID_RUN = "session_will_run";
const SESSION_ID_SKIP = "session_will_skip";

function checkIfAgentShouldRun(context: Context): Content | undefined {
  const agentName = context.agentName;
  const invocationId = context.invocationId;
  const currentState = context.state;

  console.log(`\n[Callback] Entering agent: ${agentName} (Inv: ${invocationId})`);
  console.log(`[Callback] Current State:`, currentState);

  if (currentState.get("skip_llm_agent") === true) {
    console.log(`[Callback] Skipping agent ${agentName}.`);
    return {
      parts: [{ text: `Agent ${agentName} skipped by before_agent_callback due to state.` }],
      role: "model",
    };
  } else {
    console.log(`[Callback] Proceeding with agent ${agentName}.`);
    return undefined;
  }
}

const llmAgentWithBeforeCb = new LlmAgent({
  name: "MyControlledAgent",
  model: MODEL_NAME,
  instruction: "You are a concise assistant.",
  description: "An LLM agent demonstrating stateful before_agent_callback",
  beforeAgentCallback: checkIfAgentShouldRun,
});

async function main() {
  const runner = new InMemoryRunner({ agent: llmAgentWithBeforeCb, appName: APP_NAME });

  await runner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID_RUN });
  await runner.sessionService.createSession({
    appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID_SKIP,
    state: { skip_llm_agent: true },
  });

  // Scenario 1: callback allows agent execution
  for await (const event of runner.runAsync({ userId: USER_ID, sessionId: SESSION_ID_RUN, newMessage: createUserContent("Hello, please respond.") })) {
    if (isFinalResponse(event) && event.content?.parts?.length) {
      console.log(`Final Output: [${event.author}] ${event.content.parts.map((p: any) => p.text ?? "").join("").trim()}`);
    }
  }

  // Scenario 2: callback intercepts and skips agent
  for await (const event of runner.runAsync({ userId: USER_ID, sessionId: SESSION_ID_SKIP, newMessage: createUserContent("This message won't reach the LLM.") })) {
    if (isFinalResponse(event) && event.content?.parts?.length) {
      console.log(`Final Output: [${event.author}] ${event.content.parts.map((p: any) => p.text ?? "").join("").trim()}`);
    }
  }
}

main();
```

## after_agent_callback

Checks `add_concluding_note` in session state. Returns replacement `Content` or `undefined` to pass through the agent's original output.

```typescript
import { LlmAgent, Context, isFinalResponse, InMemoryRunner } from '@google/adk';
import { createUserContent } from "@google/genai";

const MODEL_NAME = "gemini-2.5-flash";
const APP_NAME = "after_agent_callback_app";
const USER_ID = "test_user_after_agent";
const SESSION_NORMAL_ID = "session_run_normally_ts";
const SESSION_MODIFY_ID = "session_modify_output_ts";

function modifyOutputAfterAgent(context: Context): any {
  const agentName = context.agentName;
  const currentState = context.state;

  console.log(`\n[Callback] Exiting agent: ${agentName}`);
  console.log(`[Callback] Current State:`, currentState);

  if (currentState.get("add_concluding_note") === true) {
    console.log(`[Callback] Replacing agent ${agentName}'s output.`);
    return createUserContent("Concluding note added by after_agent_callback, replacing original output.");
  } else {
    console.log(`[Callback] Using agent ${agentName}'s original output.`);
    return;
  }
}

const llmAgentWithAfterCb = new LlmAgent({
  name: "MySimpleAgentWithAfter",
  model: MODEL_NAME,
  instruction: 'You are a simple agent. Just say "Processing complete!"',
  description: "An LLM agent demonstrating after_agent_callback for output modification",
  afterAgentCallback: modifyOutputAfterAgent,
});

async function main() {
  const runner = new InMemoryRunner({ agent: llmAgentWithAfterCb, appName: APP_NAME });

  await runner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: SESSION_NORMAL_ID });
  await runner.sessionService.createSession({
    appName: APP_NAME, userId: USER_ID, sessionId: SESSION_MODIFY_ID,
    state: { add_concluding_note: true },
  });

  // Scenario 1: original output is used
  for await (const event of runner.runAsync({ userId: USER_ID, sessionId: SESSION_NORMAL_ID, newMessage: createUserContent("Process this please.") })) {
    if (isFinalResponse(event) && event.content?.parts?.length) {
      console.log(`Final Output: [${event.author}] ${event.content.parts.map((p: any) => p.text ?? "").join("").trim()}`);
    }
  }

  // Scenario 2: callback replaces the agent's output
  for await (const event of runner.runAsync({ userId: USER_ID, sessionId: SESSION_MODIFY_ID, newMessage: createUserContent("Process this and add note.") })) {
    if (isFinalResponse(event) && event.content?.parts?.length) {
      console.log(`Final Output: [${event.author}] ${event.content.parts.map((p: any) => p.text ?? "").join("").trim()}`);
    }
  }
}

main();
```

## before_model_callback

Mutates `request.config.systemInstruction` and returns an LlmResponse-shaped object to block the LLM call when "BLOCK" appears in the user message, or `undefined` to proceed.

```typescript
import { LlmAgent, InMemoryRunner, Context, isFinalResponse } from '@google/adk';
import { createUserContent } from "@google/genai";

const MODEL_NAME = "gemini-2.5-flash";
const APP_NAME = "before_model_callback_app";
const USER_ID = "test_user_before_model";
const SESSION_ID_BLOCK = "session_block_model_call";
const SESSION_ID_NORMAL = "session_normal_model_call";

function simpleBeforeModelModifier({ context, request }: { context: Context; request: any }): any | undefined {
  console.log(`[Callback] Before model call for agent: ${context.agentName}`);

  const lastUserMessage = request.contents?.at(-1)?.parts?.[0]?.text ?? "";
  console.log(`[Callback] Inspecting last user message: '${lastUserMessage}'`);

  // Modification: prefix the system instruction
  const modifiedConfig = JSON.parse(JSON.stringify(request.config));
  const originalInstructionText = modifiedConfig.systemInstruction?.parts?.[0]?.text ?? "";
  const prefix = "[Modified by Callback] ";
  modifiedConfig.systemInstruction = {
    role: "system",
    parts: [{ text: prefix + originalInstructionText }],
  };
  request.config = modifiedConfig;
  console.log(`[Callback] Modified system instruction to: '${modifiedConfig.systemInstruction.parts[0].text}'`);

  // Skip: block if user message contains "BLOCK"
  if (lastUserMessage.toUpperCase().includes("BLOCK")) {
    console.log("[Callback] 'BLOCK' keyword found. Skipping LLM call.");
    return { content: { role: "model", parts: [{ text: "LLM call was blocked by the before_model_callback." }] } };
  }

  console.log("[Callback] Proceeding with LLM call.");
  return undefined;
}

const myLlmAgent = new LlmAgent({
  name: "ModelCallbackAgent",
  model: MODEL_NAME,
  instruction: "You are a helpful assistant.",
  description: "An LLM agent demonstrating before_model_callback",
  beforeModelCallback: simpleBeforeModelModifier,
});

async function callAgentAndPrint(runner: InMemoryRunner, query: string, sessionId: string) {
  console.log(`\n>>> Calling Agent with query: "${query}"`);
  let finalResponseContent = "No final response received.";
  for await (const event of runner.runAsync({ userId: USER_ID, sessionId, newMessage: createUserContent(query) })) {
    if (isFinalResponse(event) && event.content?.parts?.length) {
      finalResponseContent = event.content.parts.map((p: { text?: string }) => p.text ?? "").join("");
    }
  }
  console.log("<<< Agent Response: ", finalResponseContent);
}

async function main() {
  const runner = new InMemoryRunner({ agent: myLlmAgent, appName: APP_NAME });

  await runner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID_BLOCK });
  await callAgentAndPrint(runner, "write a joke about BLOCK", SESSION_ID_BLOCK);

  await runner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID_NORMAL });
  await callAgentAndPrint(runner, "write a short poem", SESSION_ID_NORMAL);
}

main();
```

## after_model_callback

Inspects the LLM response text and replaces occurrences of "joke" with "funny story". Returns the modified response or `undefined` to pass through unchanged.

```typescript
import { LlmAgent, InMemoryRunner, Context, isFinalResponse } from '@google/adk';
import { createUserContent } from "@google/genai";

const MODEL_NAME = "gemini-2.5-flash";
const APP_NAME = "after_model_callback_app";
const USER_ID = "test_user_after_model";
const SESSION_ID_JOKE = "session_modify_model_call";
const SESSION_ID_POEM = "session_normal_model_call";

function simpleAfterModelModifier({ context, response }: { context: Context; response: any }): any | undefined {
  console.log(`[Callback] After model call for agent: ${context.agentName}`);

  const modelResponseText = response.content?.parts?.[0]?.text ?? "";
  console.log(`[Callback] Inspecting model response: "${modelResponseText.substring(0, 50)}..."`);

  const searchTerm = "joke";
  const replaceTerm = "funny story";
  if (modelResponseText.toLowerCase().includes(searchTerm)) {
    console.log(`[Callback] Found '${searchTerm}'. Modifying response.`);
    const modifiedResponse = JSON.parse(JSON.stringify(response));
    if (modifiedResponse.content?.parts?.[0]) {
      const regex = new RegExp(searchTerm, "gi");
      modifiedResponse.content.parts[0].text = modelResponseText.replace(regex, replaceTerm);
    }
    return modifiedResponse;
  }

  console.log("[Callback] Proceeding with original LLM response.");
  return undefined;
}

const myLlmAgent = new LlmAgent({
  name: "AfterModelCallbackAgent",
  model: MODEL_NAME,
  instruction: "You are a helpful assistant who tells jokes.",
  description: "An LLM agent demonstrating after_model_callback",
  afterModelCallback: simpleAfterModelModifier,
});

async function callAgentAndPrint({ runner, query, sessionId }: { runner: InMemoryRunner; query: string; sessionId: string }) {
  console.log(`\n>>> Calling Agent with query: "${query}"`);
  let finalResponseContent = "No final response received.";
  for await (const event of runner.runAsync({ userId: USER_ID, sessionId, newMessage: createUserContent(query) })) {
    if (isFinalResponse(event) && event.content?.parts?.length) {
      finalResponseContent = event.content.parts.map((p: { text?: string }) => p.text ?? "").join("");
    }
  }
  console.log("<<< Agent Response: ", finalResponseContent);
}

async function main() {
  const runner = new InMemoryRunner({ agent: myLlmAgent, appName: APP_NAME });

  await runner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID_JOKE });
  await callAgentAndPrint({ runner, query: "write a short joke about computers", sessionId: SESSION_ID_JOKE });

  await runner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID_POEM });
  await callAgentAndPrint({ runner, query: "write a short poem about coding", sessionId: SESSION_ID_POEM });
}

main();
```

## before_tool_callback

Modifies tool `args` (redirects "Canada" to "France") or returns a result object to skip tool execution entirely when "BLOCK" is passed.

```typescript
import { LlmAgent, InMemoryRunner, FunctionTool, Context, isFinalResponse, BaseTool } from '@google/adk';
import { createUserContent } from "@google/genai";
import { z } from 'zod';

const MODEL_NAME = "gemini-2.5-flash";
const APP_NAME = "before_tool_callback_app";
const USER_ID = "test_user_before_tool";

const CountryInput = z.object({
  country: z.string().describe('The country to get the capital for.'),
});

async function getCapitalCity(params: z.infer<typeof CountryInput>): Promise<{ result: string }> {
  const capitals: Record<string, string> = {
    'united states': 'Washington, D.C.',
    'canada': 'Ottawa',
    'france': 'Paris',
    'japan': 'Tokyo',
  };
  const result = capitals[params.country.toLowerCase()] ?? `Capital not found for ${params.country}.`;
  return { result };
}

const getCapitalCityTool = new FunctionTool({
  name: 'get_capital_city',
  description: 'Retrieves the capital city for a given country',
  parameters: CountryInput,
  execute: getCapitalCity,
});

function simpleBeforeToolModifier({ tool, args, context }: { tool: BaseTool; args: Record<string, any>; context: Context }) {
  const toolName = tool.name;
  console.log(`[Callback] Before tool call for tool '${toolName}' in agent '${context.agentName}'`);
  console.log(`[Callback] Original args: ${JSON.stringify(args)}`);

  if (toolName === "get_capital_city" && args["country"]?.toLowerCase() === "canada") {
    console.log("[Callback] Detected 'Canada'. Modifying args to 'France'.");
    args["country"] = "France";
    return undefined; // proceed with modified args
  }

  if (toolName === "get_capital_city" && args["country"]?.toUpperCase() === "BLOCK") {
    console.log("[Callback] Detected 'BLOCK'. Skipping tool execution.");
    return { result: "Tool execution was blocked by before_tool_callback." };
  }

  console.log("[Callback] Proceeding with original or previously modified args.");
  return;
}

const myLlmAgent = new LlmAgent({
  name: 'ToolCallbackAgent',
  model: MODEL_NAME,
  instruction: 'You are an agent that can find capital cities. Use the get_capital_city tool.',
  description: 'An LLM agent demonstrating before_tool_callback',
  tools: [getCapitalCityTool],
  beforeToolCallback: simpleBeforeToolModifier,
});

async function callAgentAndPrint(runner: InMemoryRunner, query: string, sessionId: string) {
  console.log(`\n>>> Calling Agent for session '${sessionId}' | Query: "${query}"`);
  for await (const event of runner.runAsync({ userId: USER_ID, sessionId, newMessage: createUserContent(query) })) {
    if (isFinalResponse(event) && event.content?.parts?.length) {
      console.log(`<<< Final Output: ${event.content.parts.map(p => p.text ?? '').join('')}`);
    }
  }
}

async function main() {
  const runner = new InMemoryRunner({ agent: myLlmAgent, appName: APP_NAME });

  const canadaSessionId = 'session_canada_test';
  await runner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: canadaSessionId });
  await callAgentAndPrint(runner, 'What is the capital of Canada?', canadaSessionId);

  const blockSessionId = 'session_block_test';
  await runner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: blockSessionId });
  await callAgentAndPrint(runner, 'What is the capital of BLOCK?', blockSessionId);
}

main();
```

## after_tool_callback

Inspects the tool result object and appends a note when the capital is "Washington, D.C.". Returns the modified object or `undefined` to pass through the original.

```typescript
import { LlmAgent, InMemoryRunner, FunctionTool, isFinalResponse, Context, BaseTool } from '@google/adk';
import { createUserContent } from "@google/genai";
import { z } from "zod";

const MODEL_NAME = "gemini-2.5-flash";
const APP_NAME = "after_tool_callback_app";
const USER_ID = "test_user_after_tool";
const SESSION_ID = "session_001";

const CountryInput = z.object({
  country: z.string().describe("The country to get the capital for."),
});

async function getCapitalCity(params: z.infer<typeof CountryInput>): Promise<{ result: string }> {
  const countryCapitals: Record<string, string> = {
    "united states": "Washington, D.C.",
    "canada": "Ottawa",
    "france": "Paris",
    "germany": "Berlin",
  };
  const result = countryCapitals[params.country.toLowerCase()] ?? `Capital not found for ${params.country}`;
  return { result };
}

const capitalTool = new FunctionTool({
  name: "get_capital_city",
  description: "Retrieves the capital city for a given country",
  parameters: CountryInput,
  execute: getCapitalCity,
});

function simpleAfterToolModifier({ tool, args, context, response }: { tool: BaseTool; args: Record<string, any>; context: Context; response: Record<string, any> }) {
  const toolName = tool.name;
  console.log(`[Callback] After tool call for tool '${toolName}' in agent '${context.agentName}'`);

  const originalResultValue = response?.result || "";

  if (toolName === "get_capital_city" && originalResultValue === "Washington, D.C.") {
    const modifiedResponse = JSON.parse(JSON.stringify(response));
    modifiedResponse.result = `${originalResultValue} (Note: This is the capital of the USA).`;
    modifiedResponse["note_added_by_callback"] = true;
    console.log(`[Callback] Modified response: ${JSON.stringify(modifiedResponse)}`);
    return modifiedResponse;
  }

  console.log('[Callback] Passing original tool response through.');
  return undefined;
}

const myLlmAgent = new LlmAgent({
  name: "AfterToolCallbackAgent",
  model: MODEL_NAME,
  instruction: "You are an agent that finds capital cities using the get_capital_city tool. Report the result clearly.",
  description: "An LLM agent demonstrating after_tool_callback",
  tools: [capitalTool],
  afterToolCallback: simpleAfterToolModifier,
});

async function main() {
  const runner = new InMemoryRunner({ appName: APP_NAME, agent: myLlmAgent });

  await runner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID });

  console.log(`\n>>> Calling Agent | Query: "united states"`);
  for await (const event of runner.runAsync({ userId: USER_ID, sessionId: SESSION_ID, newMessage: createUserContent("united states") })) {
    if (isFinalResponse(event) && event.content?.parts?.length) {
      console.log(`<<< Agent Response: ${event.content.parts.map(p => p.text ?? '').join('')}`);
    }
  }
}

main();
```
