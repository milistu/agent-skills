# MCP Tools — TypeScript Examples

## Example 1: MCPToolset with StdioConnectionParams (File System)

```typescript
// agent.ts
import 'dotenv/config';
import { LlmAgent, MCPToolset } from "@google/adk";

// IMPORTANT: Replace with an actual absolute path on your system.
const TARGET_FOLDER_PATH = "/path/to/your/folder";

export const rootAgent = new LlmAgent({
    model: "gemini-2.5-flash",
    name: "filesystem_assistant_agent",
    instruction: "Help the user manage their files. You can list files, read files, etc.",
    tools: [
        // To filter tools, pass a list of tool names as the second argument:
        // new MCPToolset(connectionParams, ['list_directory', 'read_file'])
        new MCPToolset(
            {
                type: "StdioConnectionParams",
                serverParams: {
                    command: "npx",
                    args: [
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        // IMPORTANT: Must be an ABSOLUTE path the npx process can access.
                        TARGET_FOLDER_PATH,
                    ],
                },
            }
        )
    ],
});
```

## Example 2: MCPToolset with env vars (Google Maps API key)

```typescript
// agent.ts
import 'dotenv/config';
import { LlmAgent, MCPToolset } from "@google/adk";

// Load API key from environment variable.
// Run: export GOOGLE_MAPS_API_KEY="YOUR_ACTUAL_KEY"
const googleMapsApiKey = process.env.GOOGLE_MAPS_API_KEY;
if (!googleMapsApiKey) {
    throw new Error(
        'GOOGLE_MAPS_API_KEY is not provided. ' +
        'Run: export GOOGLE_MAPS_API_KEY=YOUR_ACTUAL_KEY'
    );
}

export const rootAgent = new LlmAgent({
    model: "gemini-2.5-flash",
    name: "maps_assistant_agent",
    instruction: "Help the user with mapping, directions, and finding places using Google Maps tools.",
    tools: [
        new MCPToolset(
            {
                type: "StdioConnectionParams",
                serverParams: {
                    command: "npx",
                    args: [
                        "-y",
                        "@modelcontextprotocol/server-google-maps",
                    ],
                    // Pass the API key as an environment variable to the npx subprocess
                    env: {
                        "GOOGLE_MAPS_API_KEY": googleMapsApiKey
                    }
                },
            },
            // Optional: filter for specific Maps tools:
            // ['get_directions', 'find_place_by_id']
        )
    ],
});
```

---

> **Note:** The source documentation does not include TypeScript examples for:
> - Manual async lifecycle management (section: "Using MCP Tools out of `adk web`")
> - Building an MCP server that exposes ADK tools (section 2)
> - Deployment synchronous agent definition
>
> These patterns are documented in Python only. See [mcp-tools-python.md](mcp-tools-python.md) for those examples.
