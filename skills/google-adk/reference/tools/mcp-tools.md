# Model Context Protocol Tools

> Supported in ADK: Python v0.1.0, TypeScript v0.2.0, Go v0.1.0, Java v0.1.0

This guide walks you through two ways of integrating Model Context Protocol (MCP) with ADK.

> **MCP tools for ADK:** For a list of pre-built MCP tools for ADK, see Tools and Integrations.

## What is Model Context Protocol (MCP)?

The Model Context Protocol (MCP) is an open standard designed to standardize how Large Language Models (LLMs) like Gemini and Claude communicate with external applications, data sources, and tools. Think of it as a universal connection mechanism that simplifies how LLMs obtain context, execute actions, and interact with various systems.

MCP follows a client-server architecture, defining how **data** (resources), **interactive templates** (prompts), and **actionable functions** (tools) are exposed by an **MCP server** and consumed by an **MCP client** (which could be an LLM host application or an AI agent).

This guide covers two primary integration patterns:

1. **Using Existing MCP Servers within ADK:** An ADK agent acts as an MCP client, leveraging tools provided by external MCP servers.
2. **Exposing ADK Tools via an MCP Server:** Building an MCP server that wraps ADK tools, making them accessible to any MCP client.

## Prerequisites

Before you begin, ensure you have the following set up:

- **Set up ADK:** Follow the standard ADK setup instructions in the quickstart.
- **Install/update Python/Java:** MCP requires Python 3.9 or higher, or Java 17 or higher.
- **Setup Node.js and npx:** **(Python only)** Many community MCP servers are distributed as Node.js packages and run using `npx`. Install Node.js (which includes npx) if you haven't already.
- **Verify Installations:** **(Python only)** Confirm `adk` and `npx` are in your PATH within the activated virtual environment. Both commands should print the path to the executables.

## 1. Using MCP servers with ADK agents (ADK as an MCP client) in `adk web`

This section demonstrates how to integrate tools from external MCP (Model Context Protocol) servers into your ADK agents. This is the **most common** integration pattern when your ADK agent needs to use capabilities provided by an existing service that exposes an MCP interface. You will see how the `McpToolset` class can be directly added to your agent's `tools` list, enabling seamless connection to an MCP server, discovery of its tools, and making them available for your agent to use. These examples primarily focus on interactions within the `adk web` development environment.

### `McpToolset` class

The `McpToolset` class is ADK's primary mechanism for integrating tools from an MCP server. When you include an `McpToolset` instance in your agent's `tools` list, it automatically handles the interaction with the specified MCP server. Here's how it works:

1. **Connection Management:** On initialization, `McpToolset` establishes and manages the connection to the MCP server. This can be a local server process (using `StdioConnectionParams` for communication over standard input/output) or a remote server (using `SseConnectionParams` for Server-Sent Events). The toolset also handles the graceful shutdown of this connection when the agent or application terminates.
2. **Tool Discovery & Adaptation:** Once connected, `McpToolset` queries the MCP server for its available tools (via the `list_tools` MCP method). It then converts the schemas of these discovered MCP tools into ADK-compatible `BaseTool` instances.
3. **Exposure to Agent:** These adapted tools are then made available to your `LlmAgent` as if they were native ADK tools.
4. **Proxying Tool Calls:** When your `LlmAgent` decides to use one of these tools, `McpToolset` transparently proxies the call (using the `call_tool` MCP method) to the MCP server, sends the necessary arguments, and returns the server's response back to the agent.
5. **Filtering (Optional):** You can use the `tool_filter` parameter when creating an `McpToolset` to select a specific subset of tools from the MCP server, rather than exposing all of them to your agent.

The following examples demonstrate how to use `McpToolset` within the `adk web` development environment. For scenarios where you need more fine-grained control over the MCP connection lifecycle or are not using `adk web`, refer to the "Using MCP Tools in your own Agent out of `adk web`" section later in this page.

### Example 1: File System MCP Server

This example demonstrates connecting to a local MCP server that provides file system operations.

#### Step 1: Define your Agent with `McpToolset`

Create an `agent.py` file (e.g., in `./adk_agent_samples/mcp_agent/agent.py`). The `McpToolset` is instantiated directly within the `tools` list of your `LlmAgent`.

- **Important:** Replace `"/path/to/your/folder"` in the `args` list with the **absolute path** to an actual folder on your local system that the MCP server can access.
- **Important:** Place the `.env` file in the parent directory of the `./adk_agent_samples` directory.

> *Code examples: see [mcp-tools-python.md](mcp-tools-python.md), [mcp-tools-typescript.md](mcp-tools-typescript.md), [mcp-tools-go.md](mcp-tools-go.md), [mcp-tools-java.md](mcp-tools-java.md)*

#### Step 2: Create an `__init__.py` file

Ensure you have an `__init__.py` in the same directory as `agent.py` to make it a discoverable Python package for ADK.

#### Step 3: Run `adk web` and Interact

Navigate to the parent directory of `mcp_agent` (e.g., `adk_agent_samples`) in your terminal and run `adk web`.

> **Note for Windows users:** When hitting the `_make_subprocess_transport NotImplementedError`, consider using `adk web --no-reload` instead.

Once the ADK Web UI loads in your browser:

1. Select the `filesystem_assistant_agent` from the agent dropdown.
2. Try prompts like:
   - "List files in the current directory."
   - "Can you read the file named sample.txt?" (assuming you created it in `TARGET_FOLDER_PATH`).
   - "What is the content of `another_file.md`?"

You should see the agent interacting with the MCP file system server, and the server's responses (file listings, file content) relayed through the agent. The `adk web` console (terminal where you ran the command) might also show logs from the `npx` process if it outputs to stderr.

### Example 2: Google Maps MCP Server

This example demonstrates connecting to the Google Maps MCP server.

#### Step 1: Get API Key and Enable APIs

1. **Google Maps API Key:** Follow the directions at Use API keys to obtain a Google Maps API Key.
2. **Enable APIs:** In your Google Cloud project, ensure the following APIs are enabled:
   - Directions API
   - Routes API

   For instructions, see the Getting started with Google Maps Platform documentation.

#### Step 2: Define your Agent with `McpToolset` for Google Maps

Modify your `agent.py` file (e.g., in `./adk_agent_samples/mcp_agent/agent.py`). Replace `YOUR_GOOGLE_MAPS_API_KEY` with the actual API key you obtained. It is recommended to load the key from an environment variable rather than hardcoding it. The API key is passed as an environment variable to the `npx` subprocess via the `env` parameter of `StdioServerParameters`.

> *Code examples: see [mcp-tools-python.md](mcp-tools-python.md), [mcp-tools-typescript.md](mcp-tools-typescript.md), [mcp-tools-go.md](mcp-tools-go.md), [mcp-tools-java.md](mcp-tools-java.md)*

#### Step 3: Ensure `__init__.py` Exists

If you created this in Example 1, you can skip this. Otherwise, ensure you have an `__init__.py` in the `./adk_agent_samples/mcp_agent/` directory.

#### Step 4: Run `adk web` and Interact

1. **Set Environment Variable (Recommended):** Before running `adk web`, set your Google Maps API key as an environment variable: `export GOOGLE_MAPS_API_KEY="YOUR_ACTUAL_GOOGLE_MAPS_API_KEY"`
2. **Run `adk web`:** Navigate to the parent directory of `mcp_agent` and run `adk web`.
3. **Interact in the UI:**
   - Select the `maps_assistant_agent`.
   - Try prompts like:
     - "Get directions from GooglePlex to SFO."
     - "Find coffee shops near Golden Gate Park."
     - "What's the route from Paris, France to Berlin, Germany?"

You should see the agent use the Google Maps MCP tools to provide directions or location-based information.

## 2. Building an MCP server with ADK tools (MCP server exposing ADK)

This pattern allows you to wrap existing ADK tools and make them available to any standard MCP client application. The example in this section exposes the ADK `load_web_page` tool through a custom-built MCP server.

### Summary of steps

You will create a standard Python MCP server application using the `mcp` library. Within this server, you will:

1. Instantiate the ADK tool(s) you want to expose (e.g., `FunctionTool(load_web_page)`).
2. Implement the MCP server's `@app.list_tools()` handler to advertise the ADK tool(s). This involves converting the ADK tool definition to the MCP schema using the `adk_to_mcp_tool_type` utility from `google.adk.tools.mcp_tool.conversion_utils`.
3. Implement the MCP server's `@app.call_tool()` handler. This handler will:
   - Receive tool call requests from MCP clients.
   - Identify if the request targets one of your wrapped ADK tools.
   - Execute the ADK tool's `.run_async()` method.
   - Format the ADK tool's result into an MCP-compliant response (e.g., `mcp.types.TextContent`).

### Prerequisites

Install the MCP server library in the same Python environment as your ADK installation: `pip install mcp`

### Step 1: Create the MCP Server Script

Create a new Python file for your MCP server, for example, `my_adk_mcp_server.py`.

### Step 2: Implement the Server Logic

Add the server logic to `my_adk_mcp_server.py`. This script sets up an MCP server that exposes the ADK `load_web_page` tool, using `adk_to_mcp_tool_type` for schema conversion, `@app.list_tools()` to advertise tools, and `@app.call_tool()` to proxy execution via `tool.run_async()`.

> *Code examples: see [mcp-tools-python.md](mcp-tools-python.md), [mcp-tools-typescript.md](mcp-tools-typescript.md), [mcp-tools-go.md](mcp-tools-go.md), [mcp-tools-java.md](mcp-tools-java.md)*

### Step 3: Test your Custom MCP Server with an ADK Agent

Create an ADK agent that will act as a client to the MCP server you just built. This ADK agent will use `McpToolset` to connect to your `my_adk_mcp_server.py` script.

Create an `agent.py` (e.g., in `./adk_agent_samples/mcp_client_agent/agent.py`) that uses `McpToolset` with `StdioConnectionParams` pointing to your `my_adk_mcp_server.py` script path (using `python3` as the command and the script path as the argument).

**To run the test:**

1. **Start your custom MCP server (optional, for separate observation):** You can run `my_adk_mcp_server.py` directly in one terminal to see its logs. Alternatively, `McpToolset` will start this server script as a subprocess automatically when the agent initializes.
2. **Run `adk web` for the client agent:** Navigate to the parent directory of `mcp_client_agent` and run `adk web`.
3. **Interact in the ADK Web UI:**
   - Select the `web_reader_mcp_client_agent`.
   - Try a prompt like: "Load the content from https://example.com"

The ADK agent will use `McpToolset` to start and connect to your `my_adk_mcp_server.py`. Your MCP server will receive the `call_tool` request, execute the ADK `load_web_page` tool, and return the result.

This example demonstrates how ADK tools can be encapsulated within an MCP server, making them accessible to a broader range of MCP-compliant clients, not just ADK agents.

Refer to the MCP documentation at modelcontextprotocol.io to try it out with Claude Desktop.

## Using MCP Tools in your own Agent out of `adk web`

This section is relevant to you if:

- You are developing your own Agent using ADK
- You are **NOT** using `adk web`
- You are exposing the agent via your own UI

Using MCP Tools requires a different setup than using regular tools, due to the fact that specs for MCP Tools are fetched asynchronously from the MCP Server running remotely, or in another process.

The following example is modified from "Example 1: File System MCP Server" above. The main differences are:

1. Your tool and agent are created asynchronously.
2. You need to properly manage the exit stack, so that your agents and tools are destructed properly when the connection to MCP Server is closed.

> *Code examples: see [mcp-tools-python.md](mcp-tools-python.md), [mcp-tools-typescript.md](mcp-tools-typescript.md), [mcp-tools-go.md](mcp-tools-go.md), [mcp-tools-java.md](mcp-tools-java.md)*

## Key considerations

When working with MCP and ADK, keep these points in mind:

- **Protocol vs. Library:** MCP is a protocol specification, defining communication rules. ADK is a Python library/framework for building agents. `McpToolset` bridges these by implementing the client side of the MCP protocol within the ADK framework. Conversely, building an MCP server in Python requires using the model-context-protocol library.
- **ADK Tools vs. MCP Tools:**
  - ADK Tools (`BaseTool`, `FunctionTool`, `AgentTool`, etc.) are Python objects designed for direct use within the ADK's `LlmAgent` and `Runner`.
  - MCP Tools are capabilities exposed by an MCP Server according to the protocol's schema. `McpToolset` makes these look like ADK tools to an `LlmAgent`.
- **Asynchronous nature:** Both ADK and the MCP Python library are heavily based on the `asyncio` Python library. Tool implementations and server handlers should generally be async functions.
- **Stateful sessions (MCP):** MCP establishes stateful, persistent connections between a client and server instance. This differs from typical stateless REST APIs.
  - **Deployment:** This statefulness can pose challenges for scaling and deployment, especially for remote servers handling many users. The original MCP design often assumed client and server were co-located. Managing these persistent connections requires careful infrastructure considerations (e.g., load balancing, session affinity).
  - **ADK McpToolset:** Manages this connection lifecycle. The `exit_stack` pattern shown in the examples is crucial for ensuring the connection (and potentially the server process) is properly terminated when the ADK agent finishes.

## Deploying Agents with MCP Tools

When deploying ADK agents that use MCP tools to production environments like Cloud Run, GKE, or Vertex AI Agent Engine, you need to consider how MCP connections will work in containerized and distributed environments.

### Critical Deployment Requirement: Synchronous Agent Definition

**Important:** When deploying agents with MCP tools, the agent and its `McpToolset` must be defined **synchronously** in your `agent.py` file. While `adk web` allows for asynchronous agent creation, deployment environments require synchronous instantiation. An asynchronous `get_agent()` function will not work for deployment.

> *Code examples: see [mcp-tools-python.md](mcp-tools-python.md), [mcp-tools-typescript.md](mcp-tools-typescript.md), [mcp-tools-go.md](mcp-tools-go.md), [mcp-tools-java.md](mcp-tools-java.md)*

### Quick Deployment Commands

#### Vertex AI Agent Engine

Use `uv run adk deploy agent_engine` with your GCP project ID, region, staging bucket, display name, and agent directory path.

#### Cloud Run

Use `uv run adk deploy cloud_run` with your GCP project ID, region, service name, and agent directory path.

### Deployment Patterns

#### Pattern 1: Self-Contained Stdio MCP Servers

For MCP servers that can be packaged as npm packages or Python modules (like `@modelcontextprotocol/server-filesystem`), you can include them directly in your agent container. The container must have Node.js and npm installed alongside Python. Your agent can then use `StdioConnectionParams` with `npx` commands, since `npx` and the MCP server run in the same container environment as your agent.

#### Pattern 2: Remote MCP Servers (Streamable HTTP)

For production deployments requiring scalability, deploy MCP servers as separate services and connect via Streamable HTTP. The MCP server runs as its own Cloud Run service using `StreamableHTTPSessionManager` with `stateless=True` for scalability. Your ADK agent then connects to it via `StreamableHTTPConnectionParams` with the service URL and auth headers.

#### Pattern 3: Sidecar MCP Servers (GKE)

In Kubernetes environments, you can deploy MCP servers as sidecar containers in the same pod as the main ADK agent container. The agent connects to the sidecar over `localhost` using the sidecar's container port. This provides process isolation while avoiding network overhead.

### Connection Management Considerations

#### Stdio Connections

- **Pros:** Simple setup, process isolation, works well in containers
- **Cons:** Process overhead, not suitable for high-scale deployments
- **Best for:** Development, single-tenant deployments, simple MCP servers

#### SSE/HTTP Connections

- **Pros:** Network-based, scalable, can handle multiple clients
- **Cons:** Requires network infrastructure, authentication complexity
- **Best for:** Production deployments, multi-tenant systems, external MCP services

### Production Deployment Checklist

When deploying agents with MCP tools to production:

**Connection Lifecycle**
- Ensure proper cleanup of MCP connections using exit_stack patterns
- Configure appropriate timeouts for connection establishment and requests
- Implement retry logic for transient connection failures

**Resource Management**
- Monitor memory usage for stdio MCP servers (each spawns a process)
- Configure appropriate CPU/memory limits for MCP server processes
- Consider connection pooling for remote MCP servers

**Security**
- Use authentication headers for remote MCP connections
- Restrict network access between ADK agents and MCP servers
- Filter MCP tools using `tool_filter` to limit exposed functionality
- Validate MCP tool inputs to prevent injection attacks
- Use restrictive file paths for filesystem MCP servers (e.g., `os.path.dirname(os.path.abspath(__file__))`)
- Consider read-only tool filters for production environments

**Monitoring & Observability**
- Log MCP connection establishment and teardown events
- Monitor MCP tool execution times and success rates
- Set up alerts for MCP connection failures

**Scalability**
- For high-volume deployments, prefer remote MCP servers over stdio
- Configure session affinity if using stateful MCP servers
- Consider MCP server connection limits and implement circuit breakers

### Environment-Specific Configurations

#### Cloud Run

Detect the Cloud Run environment via the `K_SERVICE` environment variable. In Cloud Run, use `SseConnectionParams` pointing to your remote MCP server URL with an auth token loaded from environment variables. For local development, fall back to `StdioConnectionParams`.

#### GKE

Use `SseConnectionParams` with Kubernetes service discovery URLs (e.g., `http://mcp-service.default.svc.cluster.local:8080/sse`).

#### Vertex AI Agent Engine

Use `SseConnectionParams` pointing to your managed MCP service URL with appropriate authorization headers.

### Troubleshooting Deployment Issues

**Common MCP Deployment Problems:**

1. **Stdio Process Startup Failures** — Add `env={'DEBUG': '1'}` to `StdioServerParameters` to get additional debug output from the subprocess.
2. **Network Connectivity Issues** — Test remote MCP server health endpoints before deploying agents that depend on them.
3. **Resource Exhaustion** — Monitor container memory usage when using stdio MCP servers. Set appropriate limits in Kubernetes deployments. Use remote MCP servers for resource-intensive operations.

## Further Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP Specification](https://modelcontextprotocol.io/specification/)
- [MCP Python SDK & Examples](https://github.com/modelcontextprotocol/)
