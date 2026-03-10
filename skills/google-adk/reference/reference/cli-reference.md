# ADK CLI documentation

This page contains the auto-generated command-line reference for ADK 1.26.0.

* [adk](#adk)

  + [api\_server](#adk-api-server)
  + [conformance](#adk-conformance)
  + [create](#adk-create)
  + [deploy](#adk-deploy)
  + [eval](#adk-eval)
  + [eval\_set](#adk-eval-set)
  + [migrate](#adk-migrate)
  + [run](#adk-run)
  + [web](#adk-web)

## [adk](#id21)

Agent Development Kit CLI tools.

Usage

```
adk [OPTIONS] COMMAND [ARGS]...
```

Options

--version
:   Show the version and exit.

### [api\_server](#id22)

Starts a FastAPI server for agents.

AGENTS\_DIR: The directory of agents, where each subdirectory is a single
agent, containing at least \_\_init\_\_.py and agent.py files.

Example:

> adk api\_server –session\_service\_uri=[uri] –port=[port] path/to/agents\_dir

Usage

```
adk api_server [OPTIONS] [AGENTS_DIR]
```

Options

--enable\_features <enable\_features>
:   Optional. Comma-separated list of feature names to enable. This provides an alternative to environment variables for enabling experimental features. Example: –enable\_features=JSON\_SCHEMA\_FOR\_FUNC\_DECL,PROGRESSIVE\_SSE\_STREAMING

--disable\_features <disable\_features>
:   Optional. Comma-separated list of feature names to disable. This provides an alternative to environment variables for disabling features. Example: –disable\_features=JSON\_SCHEMA\_FOR\_FUNC\_DECL,PROGRESSIVE\_SSE\_STREAMING

--host <host>
:   Optional. The binding host of the server

    Default:
    :   `'127.0.0.1'`

--port <port>
:   Optional. The port of the server

--allow\_origins <allow\_origins>
:   Optional. Origins to allow for CORS. Can be literal origins (e.g., ‘<https://example.com>’) or regex patterns prefixed with ‘regex:’ (e.g., ‘regex:https://.\*.example.com’).

-v, --verbose
:   Enable verbose (DEBUG) logging. Shortcut for –log\_level DEBUG.

    Default:
    :   `False`

--log\_level <log\_level>
:   Optional. Set the logging level

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

--trace\_to\_cloud
:   Optional. Whether to enable cloud trace for telemetry.

    Default:
    :   `False`

--otel\_to\_cloud
:   Optional. Whether to write OTel data to Google Cloud Observability services - Cloud Trace and Cloud Logging.

    Default:
    :   `False`

--reload, --no-reload
:   Optional. Whether to enable auto reload for server. Not supported for Cloud Run.

--a2a
:   Optional. Whether to enable A2A endpoint.

    Default:
    :   `False`

--reload\_agents
:   Optional. Whether to enable live reload for agents changes.

    Default:
    :   `False`

--eval\_storage\_uri <eval\_storage\_uri>
:   Optional. The evals storage URI to store agent evals, supported URIs: gs://<bucket name>.

--extra\_plugins <extra\_plugins>
:   Optional. Comma-separated list of extra plugin classes or instances to enable (e.g., my.module.MyPluginClass or my.module.my\_plugin\_instance).

--url\_prefix <url\_prefix>
:   Optional. URL path prefix when the application is mounted behind a reverse proxy or API gateway (e.g., ‘/api/v1’, ‘/adk’). This ensures generated URLs and redirects work correctly when the app is not served at the root path. Must start with ‘/’ if provided.

--session\_service\_uri <session\_service\_uri>
:   Optional. The URI of the session service.
    If set, ADK uses this service.

    If unset, ADK chooses a default session service (see

    –use\_local\_storage).

    - Use ‘agentengine://<agent\_engine>’ to connect to Agent Engine

    sessions. <agent\_engine> can either be the full qualified resource

    name ‘projects/abc/locations/us-central1/reasoningEngines/123’ or

    the resource id ‘123’.

    - Use ‘memory://’ to run with the in-memory session service.

    - Use ‘sqlite://<path\_to\_sqlite\_file>’ to connect to a SQLite DB.

    - See <https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls>

    for supported database URIs.

--artifact\_service\_uri <artifact\_service\_uri>
:   Optional. The URI of the artifact service.
    If set, ADK uses this service.

    If unset, ADK chooses a default artifact service (see

    –use\_local\_storage).

    - Use ‘gs://<bucket\_name>’ to connect to the GCS artifact service.

    - Use ‘memory://’ to force the in-memory artifact service.

    - Use ‘<file:/>/<path>’ to store artifacts in a custom local directory.

--use\_local\_storage, --no\_use\_local\_storage
:   Optional. Whether to use local .adk storage when –session\_service\_uri and –artifact\_service\_uri are unset. Cannot be combined with explicit service URIs. When the agents directory isn’t writable (common in Cloud Run/Kubernetes), ADK falls back to in-memory unless overridden by ADK\_FORCE\_LOCAL\_STORAGE=1 or ADK\_DISABLE\_LOCAL\_STORAGE=1.

    Default:
    :   `True`

--memory\_service\_uri <memory\_service\_uri>
:   Optional. The URI of the memory service.

    - Use ‘rag://<rag\_corpus\_id>’ to connect to Vertex AI Rag Memory Service.

    - Use ‘agentengine://<agent\_engine>’ to connect to Agent Engine

    sessions. <agent\_engine> can either be the full qualified resource

    name ‘projects/abc/locations/us-central1/reasoningEngines/123’ or

    the resource id ‘123’.

    - Use ‘memory://’ to force the in-memory memory service.

--session\_db\_url <session\_db\_url>
:   Deprecated. Use –session\_service\_uri instead.

--artifact\_storage\_uri <artifact\_storage\_uri>
:   Deprecated. Use –artifact\_service\_uri instead.

--auto\_create\_session
:   Automatically create a session if it doesn’t exist when calling /run.

Arguments

AGENTS\_DIR
:   Optional argument

### [conformance](#id23)

Conformance testing tools for ADK.

Usage

```
adk conformance [OPTIONS] COMMAND [ARGS]...
```

#### record

Generate ADK conformance test YAML files from TestCaseInput specifications.

NOTE: this is work in progress.

This command reads TestCaseInput specifications from input.yaml files,
executes the specified test cases against agents, and generates conformance
test files with recorded agent interactions as test.yaml files.

Expected directory structure:
category/name/input.yaml (TestCaseInput) -> category/name/test.yaml (TestCase)

PATHS: One or more directories containing test case specifications.
If no paths are provided, defaults to ‘tests/’ directory.

Examples:

Use default directory: adk conformance record

Custom directories: adk conformance record tests/core tests/tools

Usage

```
adk conformance record [OPTIONS] [PATHS]...
```

Arguments

PATHS
:   Optional argument(s)

#### test

Run conformance tests to verify agent behavior consistency.

Validates that agents produce consistent outputs by comparing against recorded
interactions or evaluating live execution results.

PATHS can be any number of folder paths. Each folder can either:
- Contain a spec.yaml file directly (single test case)
- Contain subdirectories with spec.yaml files (multiple test cases)

If no paths are provided, defaults to searching for the ‘tests’ folder.

TEST MODES:

replay : Verifies agent interactions match previously recorded behaviors

exactly. Compares LLM requests/responses and tool calls/results.

live : Runs evaluation-based verification (not yet implemented)

DIRECTORY STRUCTURE:

Test cases must follow this structure:

category/

test\_name/

spec.yaml # Test specification

generated-recordings.yaml # Recorded interactions (replay mode)

generated-session.yaml # Session data (replay mode)

REPORT GENERATION:

Use –generate\_report to create a Markdown report of test results.
Use –report\_dir to specify where the report should be saved.

EXAMPLES:

# Run all tests in current directory’s ‘tests’ folder

adk conformance test

# Run tests from specific folders

adk conformance test tests/core tests/tools

# Run a single test case

adk conformance test tests/core/description\_001

# Run in live mode (when available)

adk conformance test –mode=live tests/core

# Generate a test report

adk conformance test –generate\_report

# Generate a test report in a specific directory

adk conformance test –generate\_report –report\_dir=reports

Usage

```
adk conformance test [OPTIONS] [PATHS]...
```

Options

--mode <mode>
:   Test mode: ‘replay’ verifies against recorded interactions, ‘live’ runs evaluation-based verification.

    Default:
    :   `'replay'`

    Options:
    :   replay | live

--generate\_report
:   Optional. Whether to generate a Markdown report of the test results.

    Default:
    :   `False`

--report\_dir <report\_dir>
:   Optional. Directory to store the generated report. Defaults to current directory.

Arguments

PATHS
:   Optional argument(s)

### [create](#id24)

Creates a new app in the current folder with prepopulated agent template.

APP\_NAME: required, the folder of the agent source code.

Example:

> adk create path/to/my\_app

Usage

```
adk create [OPTIONS] APP_NAME
```

Options

--model <model>
:   Optional. The model used for the root agent.

--api\_key <api\_key>
:   Optional. The API Key needed to access the model, e.g. Google AI API Key.

--project <project>
:   Optional. The Google Cloud Project for using VertexAI as backend.

--region <region>
:   Optional. The Google Cloud Region for using VertexAI as backend.

Arguments

APP\_NAME
:   Required argument

### [deploy](#id25)

Deploys agent to hosted environments.

Usage

```
adk deploy [OPTIONS] COMMAND [ARGS]...
```

#### agent\_engine

Deploys an agent to Agent Engine.

Example:

> # With Express Mode API Key
> adk deploy agent\_engine –api\_key=[api\_key] my\_agent
>
> # With Google Cloud Project and Region
> adk deploy agent\_engine –project=[project] –region=[region]
>
> > –display\_name=[app\_name] my\_agent

Usage

```
adk deploy agent_engine [OPTIONS] AGENT
```

Options

--api\_key <api\_key>
:   Optional. The API key to use for Express Mode. If not provided, the API key from the GOOGLE\_API\_KEY environment variable will be used. It will only be used if GOOGLE\_GENAI\_USE\_VERTEXAI is true. (It will override GOOGLE\_API\_KEY in the .env file if it exists.)

--project <project>
:   Optional. Google Cloud project to deploy the agent. It will override GOOGLE\_CLOUD\_PROJECT in the .env file (if it exists). It will be ignored if api\_key is set.

--region <region>
:   Optional. Google Cloud region to deploy the agent. It will override GOOGLE\_CLOUD\_LOCATION in the .env file (if it exists). It will be ignored if api\_key is set.

--staging\_bucket <staging\_bucket>
:   Deprecated. This argument is no longer required or used.

--agent\_engine\_id <agent\_engine\_id>
:   Optional. ID of the Agent Engine instance to update if it exists (default: None, which means a new instance will be created). If project and region are set, this should be the resource ID, and the corresponding resource name in Agent Engine will be: projects/{project}/locations/{region}/reasoningEngines/{agent\_engine\_id}. If api\_key is set, then agent\_engine\_id is required to be the full resource name (i.e. projects/\*/locations/\*/reasoningEngines/\*).

--trace\_to\_cloud, --no-trace\_to\_cloud
:   Optional. Whether to enable Cloud Trace for Agent Engine.

--otel\_to\_cloud
:   Optional. Whether to enable OpenTelemetry for Agent Engine.

--display\_name <display\_name>
:   Optional. Display name of the agent in Agent Engine.

    Default:
    :   `''`

--description <description>
:   Optional. Description of the agent in Agent Engine.

    Default:
    :   `''`

--adk\_app <adk\_app>
:   Optional. Python file for defining the ADK application (default: a file named agent\_engine\_app.py)

--temp\_folder <temp\_folder>
:   Optional. Temp folder for the generated Agent Engine source files. If the folder already exists, its contents will be removed. (default: a timestamped folder in the current working directory).

--adk\_app\_object <adk\_app\_object>
:   Optional. Python object corresponding to the root ADK agent or app. It can only be root\_agent or app. (default: root\_agent)

--env\_file <env\_file>
:   Optional. The filepath to the .env file for environment variables. (default: the .env file in the agent directory, if any.)

--requirements\_file <requirements\_file>
:   Optional. The filepath to the requirements.txt file to use. (default: the requirements.txt file in the agent directory, if any.)

--absolutize\_imports <absolutize\_imports>
:   NOTE: This flag is deprecated and will be removed in the future.

--agent\_engine\_config\_file <agent\_engine\_config\_file>
:   Optional. The filepath to the .agent\_engine\_config.json file to use. The values in this file will be overridden by the values set by other flags. (default: the .agent\_engine\_config.json file in the agent directory, if any.)

--validate-agent-import, --no-validate-agent-import
:   Optional. Validate that the agent module can be imported before deployment. This requires your local environment to have the same dependencies as the deployment environment. (default: disabled)

--skip-agent-import-validation
:   Optional. Skip pre-deployment import validation of agent.py. This is the default; use –validate-agent-import to enable validation.

Arguments

AGENT
:   Required argument

#### cloud\_run

Deploys an agent to Cloud Run.

AGENT: The path to the agent source code folder.

Use ‘–’ to separate gcloud arguments from adk arguments.

Examples:

> adk deploy cloud\_run –project=[project] –region=[region] path/to/my\_agent
>
> adk deploy cloud\_run –project=[project] –region=[region] path/to/my\_agent
> :   – –no-allow-unauthenticated –min-instances=2

Usage

```
adk deploy cloud_run [OPTIONS] AGENT
```

Options

--project <project>
:   Required. Google Cloud project to deploy the agent. When absent, default project from gcloud config is used.

--region <region>
:   Required. Google Cloud region to deploy the agent. When absent, gcloud run deploy will prompt later.

--service\_name <service\_name>
:   Optional. The service name to use in Cloud Run (default: ‘adk-default-service-name’).

--app\_name <app\_name>
:   Optional. App name of the ADK API server (default: the folder name of the AGENT source code).

--port <port>
:   Optional. The port of the ADK API server (default: 8000).

--trace\_to\_cloud
:   Optional. Whether to enable Cloud Trace export for Cloud Run deployments.

    Default:
    :   `False`

--otel\_to\_cloud
:   Optional. Whether to enable OpenTelemetry export to GCP for Cloud Run deployments.

    Default:
    :   `False`

--with\_ui
:   Optional. Deploy ADK Web UI if set. (default: deploy ADK API server only)

    Default:
    :   `False`

--temp\_folder <temp\_folder>
:   Optional. Temp folder for the generated Cloud Run source files (default: a timestamped folder in the system temp directory).

--log\_level <log\_level>
:   Optional. Set the logging level

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

--verbosity <verbosity>
:   Deprecated. Use –log\_level instead.

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

--adk\_version <adk\_version>
:   Optional. The ADK version used in Cloud Run deployment. (default: the version in the dev environment)

    Default:
    :   `'1.26.0'`

--a2a
:   Optional. Whether to enable A2A endpoint.

    Default:
    :   `False`

--allow\_origins <allow\_origins>
:   Optional. Origins to allow for CORS. Can be literal origins (e.g., ‘<https://example.com>’) or regex patterns prefixed with ‘regex:’ (e.g., ‘regex:https://.\*.example.com’).

--session\_service\_uri <session\_service\_uri>
:   Optional. The URI of the session service.
    If set, ADK uses this service.

    If unset, ADK chooses a default session service (see

    –use\_local\_storage).

    - Use ‘agentengine://<agent\_engine>’ to connect to Agent Engine

    sessions. <agent\_engine> can either be the full qualified resource

    name ‘projects/abc/locations/us-central1/reasoningEngines/123’ or

    the resource id ‘123’.

    - Use ‘memory://’ to run with the in-memory session service.

    - Use ‘sqlite://<path\_to\_sqlite\_file>’ to connect to a SQLite DB.

    - See <https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls>

    for supported database URIs.

--artifact\_service\_uri <artifact\_service\_uri>
:   Optional. The URI of the artifact service.
    If set, ADK uses this service.

    If unset, ADK chooses a default artifact service (see

    –use\_local\_storage).

    - Use ‘gs://<bucket\_name>’ to connect to the GCS artifact service.

    - Use ‘memory://’ to force the in-memory artifact service.

    - Use ‘<file:/>/<path>’ to store artifacts in a custom local directory.

--use\_local\_storage, --no\_use\_local\_storage
:   Optional. Whether to use local .adk storage when –session\_service\_uri and –artifact\_service\_uri are unset. Cannot be combined with explicit service URIs. When the agents directory isn’t writable (common in Cloud Run/Kubernetes), ADK falls back to in-memory unless overridden by ADK\_FORCE\_LOCAL\_STORAGE=1 or ADK\_DISABLE\_LOCAL\_STORAGE=1.

    Default:
    :   `False`

--memory\_service\_uri <memory\_service\_uri>
:   Optional. The URI of the memory service.

    - Use ‘rag://<rag\_corpus\_id>’ to connect to Vertex AI Rag Memory Service.

    - Use ‘agentengine://<agent\_engine>’ to connect to Agent Engine

    sessions. <agent\_engine> can either be the full qualified resource

    name ‘projects/abc/locations/us-central1/reasoningEngines/123’ or

    the resource id ‘123’.

    - Use ‘memory://’ to force the in-memory memory service.

--session\_db\_url <session\_db\_url>
:   Deprecated. Use –session\_service\_uri instead.

--artifact\_storage\_uri <artifact\_storage\_uri>
:   Deprecated. Use –artifact\_service\_uri instead.

Arguments

AGENT
:   Required argument

#### gke

Deploys an agent to GKE.

AGENT: The path to the agent source code folder.

Example:

> adk deploy gke –project=[project] –region=[region]
> :   –cluster\_name=[cluster\_name] path/to/my\_agent

Usage

```
adk deploy gke [OPTIONS] AGENT
```

Options

--project <project>
:   Required. Google Cloud project to deploy the agent. When absent, default project from gcloud config is used.

--region <region>
:   Required. Google Cloud region to deploy the agent. When absent, gcloud run deploy will prompt later.

--cluster\_name <cluster\_name>
:   Required. The name of the GKE cluster.

--service\_name <service\_name>
:   Optional. The service name to use in GKE (default: ‘adk-default-service-name’).

--app\_name <app\_name>
:   Optional. App name of the ADK API server (default: the folder name of the AGENT source code).

--port <port>
:   Optional. The port of the ADK API server (default: 8000).

--trace\_to\_cloud
:   Optional. Whether to enable Cloud Trace for GKE.

    Default:
    :   `False`

--otel\_to\_cloud
:   Optional. Whether to enable OpenTelemetry for GKE.

    Default:
    :   `False`

--with\_ui
:   Optional. Deploy ADK Web UI if set. (default: deploy ADK API server only)

    Default:
    :   `False`

--log\_level <log\_level>
:   Optional. Set the logging level

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

--temp\_folder <temp\_folder>
:   Optional. Temp folder for the generated GKE source files (default: a timestamped folder in the system temp directory).

--adk\_version <adk\_version>
:   Optional. The ADK version used in GKE deployment. (default: the version in the dev environment)

    Default:
    :   `'1.26.0'`

--session\_service\_uri <session\_service\_uri>
:   Optional. The URI of the session service.
    If set, ADK uses this service.

    If unset, ADK chooses a default session service (see

    –use\_local\_storage).

    - Use ‘agentengine://<agent\_engine>’ to connect to Agent Engine

    sessions. <agent\_engine> can either be the full qualified resource

    name ‘projects/abc/locations/us-central1/reasoningEngines/123’ or

    the resource id ‘123’.

    - Use ‘memory://’ to run with the in-memory session service.

    - Use ‘sqlite://<path\_to\_sqlite\_file>’ to connect to a SQLite DB.

    - See <https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls>

    for supported database URIs.

--artifact\_service\_uri <artifact\_service\_uri>
:   Optional. The URI of the artifact service.
    If set, ADK uses this service.

    If unset, ADK chooses a default artifact service (see

    –use\_local\_storage).

    - Use ‘gs://<bucket\_name>’ to connect to the GCS artifact service.

    - Use ‘memory://’ to force the in-memory artifact service.

    - Use ‘<file:/>/<path>’ to store artifacts in a custom local directory.

--use\_local\_storage, --no\_use\_local\_storage
:   Optional. Whether to use local .adk storage when –session\_service\_uri and –artifact\_service\_uri are unset. Cannot be combined with explicit service URIs. When the agents directory isn’t writable (common in Cloud Run/Kubernetes), ADK falls back to in-memory unless overridden by ADK\_FORCE\_LOCAL\_STORAGE=1 or ADK\_DISABLE\_LOCAL\_STORAGE=1.

    Default:
    :   `False`

--memory\_service\_uri <memory\_service\_uri>
:   Optional. The URI of the memory service.

    - Use ‘rag://<rag\_corpus\_id>’ to connect to Vertex AI Rag Memory Service.

    - Use ‘agentengine://<agent\_engine>’ to connect to Agent Engine

    sessions. <agent\_engine> can either be the full qualified resource

    name ‘projects/abc/locations/us-central1/reasoningEngines/123’ or

    the resource id ‘123’.

    - Use ‘memory://’ to force the in-memory memory service.

Arguments

AGENT
:   Required argument

### [eval](#id26)

Evaluates an agent given the eval sets.

AGENT\_MODULE\_FILE\_PATH: The path to the \_\_init\_\_.py file that contains a
module by the name “agent”. “agent” module contains a root\_agent.

EVAL\_SET\_FILE\_PATH\_OR\_ID: You can specify one or more eval set file paths or
eval set id.

Mixing of eval set file paths with eval set ids is not allowed.

*Eval Set File Path*
For each file, all evals will be run by default.

If you want to run only specific evals from an eval set, first create a comma
separated list of eval names and then add that as a suffix to the eval set
file name, demarcated by a :.

For example, we have sample\_eval\_set\_file.json file that has following the
eval cases:
sample\_eval\_set\_file.json:

> [|](#id1)……. eval\_1
> [|](#id3)……. eval\_2
> [|](#id5)……. eval\_3
> [|](#id7)……. eval\_4
> [|](#id9)……. eval\_5

sample\_eval\_set\_file.json:eval\_1,eval\_2,eval\_3

This will only run eval\_1, eval\_2 and eval\_3 from sample\_eval\_set\_file.json.

*Eval Set ID*
For each eval set, all evals will be run by default.

If you want to run only specific evals from an eval set, first create a comma
separated list of eval names and then add that as a suffix to the eval set
file name, demarcated by a :.

For example, we have sample\_eval\_set\_id that has following the eval cases:
sample\_eval\_set\_id:

> [|](#id11)……. eval\_1
> [|](#id13)……. eval\_2
> [|](#id15)……. eval\_3
> [|](#id17)……. eval\_4
> [|](#id19)……. eval\_5

If we did:
:   sample\_eval\_set\_id:eval\_1,eval\_2,eval\_3

This will only run eval\_1, eval\_2 and eval\_3 from sample\_eval\_set\_id.

CONFIG\_FILE\_PATH: The path to config file.

PRINT\_DETAILED\_RESULTS: Prints detailed results on the console.

Usage

```
adk eval [OPTIONS] AGENT_MODULE_FILE_PATH [EVAL_SET_FILE_PATH_OR_ID]...
```

Options

--enable\_features <enable\_features>
:   Optional. Comma-separated list of feature names to enable. This provides an alternative to environment variables for enabling experimental features. Example: –enable\_features=JSON\_SCHEMA\_FOR\_FUNC\_DECL,PROGRESSIVE\_SSE\_STREAMING

--disable\_features <disable\_features>
:   Optional. Comma-separated list of feature names to disable. This provides an alternative to environment variables for disabling features. Example: –disable\_features=JSON\_SCHEMA\_FOR\_FUNC\_DECL,PROGRESSIVE\_SSE\_STREAMING

--config\_file\_path <config\_file\_path>
:   Optional. The path to config file.

--print\_detailed\_results
:   Optional. Whether to print detailed results on console or not.

    Default:
    :   `False`

--eval\_storage\_uri <eval\_storage\_uri>
:   Optional. The evals storage URI to store agent evals, supported URIs: gs://<bucket name>.

--log\_level <log\_level>
:   Optional. Set the logging level

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

Arguments

AGENT\_MODULE\_FILE\_PATH
:   Required argument

EVAL\_SET\_FILE\_PATH\_OR\_ID
:   Optional argument(s)

### [eval\_set](#id27)

Manage Eval Sets.

Usage

```
adk eval_set [OPTIONS] COMMAND [ARGS]...
```

#### add\_eval\_case

Adds eval cases to the given eval set.

There are several ways that an eval case can be created, for now this method
only supports adding one using a conversation scenarios file.

If an eval case for the generated id already exists, then we skip adding it.

Usage

```
adk eval_set add_eval_case [OPTIONS] AGENT_MODULE_FILE_PATH EVAL_SET_ID
```

Options

--scenarios\_file <scenarios\_file>
:   **Required** A path to file containing JSON serialized ConversationScenarios.

--session\_input\_file <session\_input\_file>
:   **Required** Path to session file containing SessionInput in JSON format.

--eval\_storage\_uri <eval\_storage\_uri>
:   Optional. The evals storage URI to store agent evals, supported URIs: gs://<bucket name>.

--log\_level <log\_level>
:   Optional. Set the logging level

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

Arguments

AGENT\_MODULE\_FILE\_PATH
:   Required argument

EVAL\_SET\_ID
:   Required argument

#### create

Creates an empty EvalSet given the agent\_module\_file\_path and eval\_set\_id.

Usage

```
adk eval_set create [OPTIONS] AGENT_MODULE_FILE_PATH EVAL_SET_ID
```

Options

--eval\_storage\_uri <eval\_storage\_uri>
:   Optional. The evals storage URI to store agent evals, supported URIs: gs://<bucket name>.

--log\_level <log\_level>
:   Optional. Set the logging level

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

Arguments

AGENT\_MODULE\_FILE\_PATH
:   Required argument

EVAL\_SET\_ID
:   Required argument

### [migrate](#id28)

ADK migration commands.

Usage

```
adk migrate [OPTIONS] COMMAND [ARGS]...
```

#### session

Migrates a session database to the latest schema version.

Usage

```
adk migrate session [OPTIONS]
```

Options

--source\_db\_url <source\_db\_url>
:   **Required** SQLAlchemy URL of source database in database session service, e.g. sqlite:///source.db.

--dest\_db\_url <dest\_db\_url>
:   **Required** SQLAlchemy URL of destination database in database session service, e.g. sqlite:///dest.db.

--log\_level <log\_level>
:   Optional. Set the logging level

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

### [run](#id29)

Runs an interactive CLI for a certain agent.

AGENT: The path to the agent source code folder.

Example:

> adk run path/to/my\_agent

Usage

```
adk run [OPTIONS] AGENT
```

Options

--enable\_features <enable\_features>
:   Optional. Comma-separated list of feature names to enable. This provides an alternative to environment variables for enabling experimental features. Example: –enable\_features=JSON\_SCHEMA\_FOR\_FUNC\_DECL,PROGRESSIVE\_SSE\_STREAMING

--disable\_features <disable\_features>
:   Optional. Comma-separated list of feature names to disable. This provides an alternative to environment variables for disabling features. Example: –disable\_features=JSON\_SCHEMA\_FOR\_FUNC\_DECL,PROGRESSIVE\_SSE\_STREAMING

--session\_service\_uri <session\_service\_uri>
:   Optional. The URI of the session service.
    If set, ADK uses this service.

    If unset, ADK chooses a default session service (see

    –use\_local\_storage).

    - Use ‘agentengine://<agent\_engine>’ to connect to Agent Engine

    sessions. <agent\_engine> can either be the full qualified resource

    name ‘projects/abc/locations/us-central1/reasoningEngines/123’ or

    the resource id ‘123’.

    - Use ‘memory://’ to run with the in-memory session service.

    - Use ‘sqlite://<path\_to\_sqlite\_file>’ to connect to a SQLite DB.

    - See <https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls>

    for supported database URIs.

--artifact\_service\_uri <artifact\_service\_uri>
:   Optional. The URI of the artifact service.
    If set, ADK uses this service.

    If unset, ADK chooses a default artifact service (see

    –use\_local\_storage).

    - Use ‘gs://<bucket\_name>’ to connect to the GCS artifact service.

    - Use ‘memory://’ to force the in-memory artifact service.

    - Use ‘<file:/>/<path>’ to store artifacts in a custom local directory.

--use\_local\_storage, --no\_use\_local\_storage
:   Optional. Whether to use local .adk storage when –session\_service\_uri and –artifact\_service\_uri are unset. Cannot be combined with explicit service URIs. When the agents directory isn’t writable (common in Cloud Run/Kubernetes), ADK falls back to in-memory unless overridden by ADK\_FORCE\_LOCAL\_STORAGE=1 or ADK\_DISABLE\_LOCAL\_STORAGE=1.

    Default:
    :   `True`

--memory\_service\_uri <memory\_service\_uri>
:   Optional. The URI of the memory service.

    - Use ‘rag://<rag\_corpus\_id>’ to connect to Vertex AI Rag Memory Service.

    - Use ‘agentengine://<agent\_engine>’ to connect to Agent Engine

    sessions. <agent\_engine> can either be the full qualified resource

    name ‘projects/abc/locations/us-central1/reasoningEngines/123’ or

    the resource id ‘123’.

    - Use ‘memory://’ to force the in-memory memory service.

--save\_session
:   Optional. Whether to save the session to a json file on exit.

    Default:
    :   `False`

--session\_id <session\_id>
:   Optional. The session ID to save the session to on exit when –save\_session is set to true. User will be prompted to enter a session ID if not set.

--replay <replay>
:   The json file that contains the initial state of the session and user queries. A new session will be created using this state. And user queries are run against the newly created session. Users cannot continue to interact with the agent.

--resume <resume>
:   The json file that contains a previously saved session (by –save\_session option). The previous session will be re-displayed. And user can continue to interact with the agent.

Arguments

AGENT
:   Required argument

### [web](#id30)

Starts a FastAPI server with Web UI for agents.

AGENTS\_DIR: The directory of agents, where each subdirectory is a single
agent, containing at least \_\_init\_\_.py and agent.py files.

Example:

> adk web –session\_service\_uri=[uri] –port=[port] path/to/agents\_dir

Usage

```
adk web [OPTIONS] [AGENTS_DIR]
```

Options

--enable\_features <enable\_features>
:   Optional. Comma-separated list of feature names to enable. This provides an alternative to environment variables for enabling experimental features. Example: –enable\_features=JSON\_SCHEMA\_FOR\_FUNC\_DECL,PROGRESSIVE\_SSE\_STREAMING

--disable\_features <disable\_features>
:   Optional. Comma-separated list of feature names to disable. This provides an alternative to environment variables for disabling features. Example: –disable\_features=JSON\_SCHEMA\_FOR\_FUNC\_DECL,PROGRESSIVE\_SSE\_STREAMING

--host <host>
:   Optional. The binding host of the server

    Default:
    :   `'127.0.0.1'`

--port <port>
:   Optional. The port of the server

--allow\_origins <allow\_origins>
:   Optional. Origins to allow for CORS. Can be literal origins (e.g., ‘<https://example.com>’) or regex patterns prefixed with ‘regex:’ (e.g., ‘regex:https://.\*.example.com’).

-v, --verbose
:   Enable verbose (DEBUG) logging. Shortcut for –log\_level DEBUG.

    Default:
    :   `False`

--log\_level <log\_level>
:   Optional. Set the logging level

    Options:
    :   DEBUG | INFO | WARNING | ERROR | CRITICAL

--trace\_to\_cloud
:   Optional. Whether to enable cloud trace for telemetry.

    Default:
    :   `False`

--otel\_to\_cloud
:   Optional. Whether to write OTel data to Google Cloud Observability services - Cloud Trace and Cloud Logging.

    Default:
    :   `False`

--reload, --no-reload
:   Optional. Whether to enable auto reload for server. Not supported for Cloud Run.

--a2a
:   Optional. Whether to enable A2A endpoint.

    Default:
    :   `False`

--reload\_agents
:   Optional. Whether to enable live reload for agents changes.

    Default:
    :   `False`

--eval\_storage\_uri <eval\_storage\_uri>
:   Optional. The evals storage URI to store agent evals, supported URIs: gs://<bucket name>.

--extra\_plugins <extra\_plugins>
:   Optional. Comma-separated list of extra plugin classes or instances to enable (e.g., my.module.MyPluginClass or my.module.my\_plugin\_instance).

--url\_prefix <url\_prefix>
:   Optional. URL path prefix when the application is mounted behind a reverse proxy or API gateway (e.g., ‘/api/v1’, ‘/adk’). This ensures generated URLs and redirects work correctly when the app is not served at the root path. Must start with ‘/’ if provided.

--logo-text <logo\_text>
:   Optional. The text to display in the logo of the web UI.

--logo-image-url <logo\_image\_url>
:   Optional. The URL of the image to display in the logo of the web UI.

--session\_service\_uri <session\_service\_uri>
:   Optional. The URI of the session service.
    If set, ADK uses this service.

    If unset, ADK chooses a default session service (see

    –use\_local\_storage).

    - Use ‘agentengine://<agent\_engine>’ to connect to Agent Engine

    sessions. <agent\_engine> can either be the full qualified resource

    name ‘projects/abc/locations/us-central1/reasoningEngines/123’ or

    the resource id ‘123’.

    - Use ‘memory://’ to run with the in-memory session service.

    - Use ‘sqlite://<path\_to\_sqlite\_file>’ to connect to a SQLite DB.

    - See <https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls>

    for supported database URIs.

--artifact\_service\_uri <artifact\_service\_uri>
:   Optional. The URI of the artifact service.
    If set, ADK uses this service.

    If unset, ADK chooses a default artifact service (see

    –use\_local\_storage).

    - Use ‘gs://<bucket\_name>’ to connect to the GCS artifact service.

    - Use ‘memory://’ to force the in-memory artifact service.

    - Use ‘<file:/>/<path>’ to store artifacts in a custom local directory.

--use\_local\_storage, --no\_use\_local\_storage
:   Optional. Whether to use local .adk storage when –session\_service\_uri and –artifact\_service\_uri are unset. Cannot be combined with explicit service URIs. When the agents directory isn’t writable (common in Cloud Run/Kubernetes), ADK falls back to in-memory unless overridden by ADK\_FORCE\_LOCAL\_STORAGE=1 or ADK\_DISABLE\_LOCAL\_STORAGE=1.

    Default:
    :   `True`

--memory\_service\_uri <memory\_service\_uri>
:   Optional. The URI of the memory service.

    - Use ‘rag://<rag\_corpus\_id>’ to connect to Vertex AI Rag Memory Service.

    - Use ‘agentengine://<agent\_engine>’ to connect to Agent Engine

    sessions. <agent\_engine> can either be the full qualified resource

    name ‘projects/abc/locations/us-central1/reasoningEngines/123’ or

    the resource id ‘123’.

    - Use ‘memory://’ to force the in-memory memory service.

--session\_db\_url <session\_db\_url>
:   Deprecated. Use –session\_service\_uri instead.

--artifact\_storage\_uri <artifact\_storage\_uri>
:   Deprecated. Use –artifact\_service\_uri instead.

Arguments

AGENTS\_DIR
:   Optional argument