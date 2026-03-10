# Use the Command Line


ADK provides an interactive terminal interface for testing your agents. This is
useful for quick testing, scripted interactions, and CI/CD pipelines.


## Run an agent

Use the following command to run your agent in the ADK command line interface:


```
adk run my_agent
```

Create an `AgentCliRunner` class (see Java Quickstart) and run:

```
mvn compile exec:java -Dexec.mainClass="com.example.agent.AgentCliRunner"
```

This starts an interactive session where you can type queries and see agent
responses directly in your terminal:

```
Running agent my_agent, type exit to exit.
[user]: What's the weather in New York?
[my_agent]: The weather in New York is sunny with a temperature of 25°C.
[user]: exit
```

## Session options

The `adk run` command includes options for saving, resuming, and replaying
sessions.

### Save sessions

To save the session when you exit:

```
adk run --save_session path/to/my_agent
```

You'll be prompted to enter a session ID, and the session will be saved to
`path/to/my_agent/<session_id>.session.json`.

You can also specify the session ID upfront:

```
adk run --save_session --session_id my_session path/to/my_agent
```

### Resume sessions

To continue a previously saved session:

```
adk run --resume path/to/my_agent/my_session.session.json path/to/my_agent
```

This loads the previous session state and event history, displays it, and allows
you to continue the conversation.

### Replay sessions

To replay a session file without interactive input:

```
adk run --replay path/to/input.json path/to/my_agent
```

The input file should contain initial state and queries:

```
{
  "state": {"key": "value"},
  "queries": ["What is 2 + 2?", "What is the capital of France?"]
}
```

## Storage options

| Option | Description | Default |
| --- | --- | --- |
| `--session_service_uri` | Custom session storage URI | SQLite under `.adk/session.db` |
| `--artifact_service_uri` | Custom artifact storage URI | Local `.adk/artifacts` |

### Example with storage options

```
adk run --session_service_uri "sqlite:///my_sessions.db" path/to/my_agent
```

## All options

| Option | Description |
| --- | --- |
| `--save_session` | Save the session to a JSON file on exit |
| `--session_id` | Session ID to use when saving |
| `--resume` | Path to a saved session file to resume |
| `--replay` | Path to an input file for non-interactive replay |
| `--session_service_uri` | Custom session storage URI |
| `--artifact_service_uri` | Custom artifact storage URI |