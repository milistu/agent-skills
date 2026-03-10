# LLM Agent — TypeScript Examples

## Instructions with State Templating

Demonstrates passing a multi-line instruction string with `{var}` template placeholders to `LlmAgent`.

```typescript
const capitalAgent = new LlmAgent({
    model: 'gemini-2.5-flash',
    name: 'capital_agent',
    description: 'Answers user questions about the capital city of a given country.',
    instruction: `You are an agent that provides the capital city of a country.
        When a user asks for the capital of a country:
        1. Identify the country name from the user's query.
        2. Use the \`getCapitalCity\` tool to find the capital.
        3. Respond clearly to the user, stating the capital city.
        Example Query: "What's the capital of {country}?"
        Example Response: "The capital of France is Paris."
        `,
    // tools will be added next
});
```

## Equipping the Agent: Tools

Demonstrates defining a FunctionTool with a Zod parameter schema and wiring it into `LlmAgent`; TypeScript requires explicit FunctionTool wrapping (unlike Python's auto-wrap).

```typescript
import { z } from 'zod';
import { LlmAgent, FunctionTool } from '@google/adk';

// Define parameter schema using Zod
const getCapitalCityParamsSchema = z.object({
    country: z.string().describe('The country to get capital for.'),
});

// Define the tool function
async function getCapitalCity(
    params: z.infer<typeof getCapitalCityParamsSchema>
): Promise<{ capitalCity: string }> {
    const capitals: Record<string, string> = {
        'france': 'Paris',
        'japan': 'Tokyo',
        'canada': 'Ottawa',
    };
    const result = capitals[params.country.toLowerCase()] ??
        `Sorry, I don't know the capital of ${params.country}.`;
    return { capitalCity: result }; // Tools must return an object
}

// Wrap as a FunctionTool
const getCapitalCityTool = new FunctionTool({
    name: 'getCapitalCity',
    description: 'Retrieves the capital city for a given country.',
    parameters: getCapitalCityParamsSchema,
    execute: getCapitalCity,
});

const capitalAgent = new LlmAgent({
    model: 'gemini-2.5-flash',
    name: 'capitalAgent',
    description: 'Answers user questions about the capital city of a given country.',
    instruction: 'You are an agent that provides the capital city of a country...',
    tools: [getCapitalCityTool],
});
```

## Fine-Tuning LLM Generation (`generateContentConfig`)

Demonstrates passing `GenerateContentConfig` to control temperature and max output tokens.

```typescript
import { GenerateContentConfig } from '@google/genai';

const generateContentConfig: GenerateContentConfig = {
    temperature: 0.2, // More deterministic output
    maxOutputTokens: 250,
};

const agent = new LlmAgent({
    // ... other params
    generateContentConfig,
});
```

## Structured Output (`outputSchema` + `outputKey`)

Demonstrates using an ADK `Schema` object as `outputSchema` to enforce JSON output and `outputKey` to store the result in session state. Tools cannot be used alongside `outputSchema`.

```typescript
import { Schema, Type } from '@google/genai';

const CapitalInfoOutputSchema: Schema = {
    type: Type.OBJECT,
    description: "Schema for capital city information.",
    properties: {
        capital: {
            type: Type.STRING,
            description: "The capital city of the country.",
        },
        population_estimate: {
            type: Type.STRING,
            description: "An estimated population of the capital city.",
        },
    },
    required: ["capital", "population_estimate"],
};

const structuredInfoAgentSchema = new LlmAgent({
    // ... name, model, description
    instruction: `You are an agent that provides country information.
Respond ONLY with a JSON object matching this exact schema:
${JSON.stringify(CapitalInfoOutputSchema, null, 2)}
Use your knowledge to determine the capital and estimate the population. Do not use any tools.
`,
    outputSchema: CapitalInfoOutputSchema, // Enforce JSON output
    outputKey: "structured_info_result",   // Store result in session state
    // *** NO tools parameter here - using outputSchema prevents tool use ***
});
```

## Putting It Together: Full End-to-End Example

Full runnable example contrasting two agents: one uses a tool + `outputKey`, the other uses `outputSchema` + `outputKey` (no tools). Shows FunctionTool, `InMemoryRunner`, session creation, async event iteration, and reading back session state.

```typescript
import { LlmAgent, FunctionTool, InMemoryRunner, isFinalResponse } from '@google/adk';
import { createUserContent, Schema, Type } from '@google/genai';
import type { Part } from '@google/genai';
import { z } from 'zod';

const APP_NAME = "capital_app_ts";
const USER_ID = "test_user_789";
const SESSION_ID_TOOL_AGENT = "session_tool_agent_ts";
const SESSION_ID_SCHEMA_AGENT = "session_schema_agent_ts";
const MODEL_NAME = "gemini-2.5-flash";

// --- Schemas ---

const CountryInput = z.object({
    country: z.string().describe('The country to get the capital for.'),
});

const CapitalInfoOutputSchema: Schema = {
    type: Type.OBJECT,
    description: "Schema for capital city information.",
    properties: {
        capital: { type: Type.STRING, description: "The capital city of the country." },
        population_estimate: { type: Type.STRING, description: "An estimated population of the capital city." },
    },
    required: ["capital", "population_estimate"],
};

// --- Tool ---

async function getCapitalCity(params: z.infer<typeof CountryInput>): Promise<{ result: string }> {
    console.log(`\n-- Tool Call: getCapitalCity(country='${params.country}') --`);
    const capitals: Record<string, string> = {
        'united states': 'Washington, D.C.',
        'canada': 'Ottawa',
        'france': 'Paris',
        'japan': 'Tokyo',
    };
    const result = capitals[params.country.toLowerCase()] ??
        `Sorry, I couldn't find the capital for ${params.country}.`;
    console.log(`-- Tool Result: '${result}' --`);
    return { result };
}

const getCapitalCityTool = new FunctionTool({
    name: 'get_capital_city',
    description: 'Retrieves the capital city for a given country',
    parameters: CountryInput,
    execute: getCapitalCity,
});

// --- Agent 1: Uses a tool and outputKey ---
const capitalAgentWithTool = new LlmAgent({
    model: MODEL_NAME,
    name: 'capital_agent_tool',
    description: 'Retrieves the capital city using a specific tool.',
    instruction: `You are a helpful agent that provides the capital city of a country using a tool.
The user will provide the country name in a JSON format like {"country": "country_name"}.
1. Extract the country name.
2. Use the get_capital_city tool to find the capital.
3. Respond with the capital city.
`,
    tools: [getCapitalCityTool],
    outputKey: "capital_tool_result",
});

// --- Agent 2: Uses outputSchema (NO tools possible) ---
const structuredInfoAgentSchema = new LlmAgent({
    model: MODEL_NAME,
    name: 'structured_info_agent_schema',
    description: 'Provides capital and estimated population in a specific JSON format.',
    instruction: `You are an agent that provides country information.
The user will provide the country name in a JSON format like {"country": "country_name"}.
Respond ONLY with a JSON object. Use your knowledge. Do not use any tools.
`,
    outputSchema: CapitalInfoOutputSchema,
    outputKey: "structured_info_result",
});

// --- Interaction helper ---
async function callAgentAndPrint(
    runner: InMemoryRunner,
    agent: LlmAgent,
    sessionId: string,
    queryJson: string
) {
    console.log(`\n>>> Calling Agent: '${agent.name}' | Query: ${queryJson}`);
    const message = createUserContent(queryJson);

    let finalResponseContent = "No final response received.";
    for await (const event of runner.runAsync({ userId: USER_ID, sessionId, newMessage: message })) {
        if (isFinalResponse(event) && event.content?.parts?.length) {
            finalResponseContent = event.content.parts.map((part: Part) => part.text ?? '').join('');
        }
    }
    console.log(`<<< Agent '${agent.name}' Response: ${finalResponseContent}`);

    const currentSession = await runner.sessionService.getSession({
        appName: APP_NAME, userId: USER_ID, sessionId,
    });
    if (!currentSession) { console.log(`--- Session not found: ${sessionId} ---`); return; }

    const storedOutput = currentSession.state[agent.outputKey!];
    console.log(`--- Session State ['${agent.outputKey}']: `);
    try {
        console.log(JSON.stringify(JSON.parse(storedOutput as string), null, 2));
    } catch (e) {
        console.log(storedOutput);
    }
    console.log("-".repeat(30));
}

// --- Main ---
async function main() {
    const capitalRunner = new InMemoryRunner({ appName: APP_NAME, agent: capitalAgentWithTool });
    const structuredRunner = new InMemoryRunner({ appName: APP_NAME, agent: structuredInfoAgentSchema });

    console.log("--- Creating Sessions ---");
    await capitalRunner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID_TOOL_AGENT });
    await structuredRunner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID_SCHEMA_AGENT });

    console.log("\n--- Testing Agent with Tool ---");
    await callAgentAndPrint(capitalRunner, capitalAgentWithTool, SESSION_ID_TOOL_AGENT, '{"country": "France"}');
    await callAgentAndPrint(capitalRunner, capitalAgentWithTool, SESSION_ID_TOOL_AGENT, '{"country": "Canada"}');

    console.log("\n--- Testing Agent with Output Schema (No Tool Use) ---");
    await callAgentAndPrint(structuredRunner, structuredInfoAgentSchema, SESSION_ID_SCHEMA_AGENT, '{"country": "France"}');
    await callAgentAndPrint(structuredRunner, structuredInfoAgentSchema, SESSION_ID_SCHEMA_AGENT, '{"country": "Japan"}');
}

main();
```
