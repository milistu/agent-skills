# Agent Runtime


ADK provides several ways to run and test your agents during development. Choose
the method that best fits your development workflow.

## Ways to run agents

* **Dev UI**

  ---

  Use `adk web` to launch a browser-based interface for interacting with your
  agents.

  Use the Web Interface
* **Command Line**

  ---

  Use `adk run` to interact with your agents directly in the terminal.

  Use the Command Line
* **API Server**

  ---

  Use `adk api_server` to expose your agents through a RESTful API.

  Use the API Server

## Technical reference

For more in-depth information on runtime configuration and behavior, see these
pages:

* **Event Loop**: Understand the core event loop that powers
  ADK, including the yield/pause/resume cycle.
* **Resume Agents**: Learn how to resume agent execution from a
  previous state.
* **Runtime Config**: Configure runtime behavior with
  RunConfig.