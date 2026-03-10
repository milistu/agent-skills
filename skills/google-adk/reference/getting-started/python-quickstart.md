# Python Quickstart for ADK

This guide shows you how to get up and running with Agent Development Kit
(ADK) for Python. Before you start, make sure you have the following installed:

* Python 3.10 or later
* `pip` for installing packages

## Installation

Install ADK by running the following command:

```
pip install google-adk
```

Recommended: create and activate a Python virtual environment

Create a Python virtual environment:

```
python -m venv .venv
```

Activate the Python virtual environment:


```
.venv\Scripts\activate.bat
```

## Create an agent project

Run the `adk create` command to start a new agent project.

```
adk create my_agent
```

### Explore the agent project

The created agent project has the following structure, with the `agent.py`
file containing the main control code for the agent.

```
my_agent/
    agent.py      # main agent code
    .env          # API keys or project IDs
    __init__.py
```

## Update your agent project

The `agent.py` file contains a `root_agent` definition which is the only
required element of an ADK agent. You can also define tools for the agent to
use. Update the generated `agent.py` code to include a `get_current_time` tool
for use by the agent, as shown in the following code:

```
from google.adk.agents.llm_agent import Agent

# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = Agent(
    model='gemini-3-flash-preview',
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)
```

### Set your API key

This project uses the Gemini API, which requires an API key. If you
don't already have Gemini API key, create a key in Google AI Studio on the
[API Keys](https://aistudio.google.com/app/apikey) page.

In a terminal window, write your API key into an `.env` file as an environment variable:

Update: my\_agent/.env

```
echo 'GOOGLE_API_KEY="YOUR_API_KEY"' > .env
```

Using other AI models with ADK

ADK supports the use of many generative AI models. For more
information on configuring other models in ADK agents, see
Models & Authentication.

## Run your agent

You can run your ADK agent with an interactive command-line interface using the
`adk run` command or the ADK web user interface provided by the ADK using the
`adk web` command. Both these options allow you to test and interact with your
agent.

### Run with command-line interface

Run your agent using the `adk run` command-line tool.

```
adk run my_agent
```


### Run with web interface

The ADK framework provides web interface you can use to test and interact with
your agent. You can start the web interface using the following command:

```
adk web --port 8000
```


Run this command from the **parent directory** that contains your
`my_agent/` folder. For example, if your agent is inside `agents/my_agent/`,
run `adk web` from the `agents/` directory.

This command starts a web server with a chat interface for your agent. You can
access the web interface at (http://localhost:8000). Select the agent at the
upper left corner and type a request.


Caution: ADK Web for development only

ADK Web is ***not meant for use in production deployments***. You should
use ADK Web for development and debugging purposes only.