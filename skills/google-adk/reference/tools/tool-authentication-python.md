# Tool Authentication — Python Examples

> Source: https://google.github.io/adk-docs/tools-custom/authentication/
> Language: Python

---

## 1. API Key Auth — `token_to_scheme_credential()`

```python
from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

auth_scheme, auth_credential = token_to_scheme_credential(
    "apikey", "query", "apikey", "YOUR_API_KEY_STRING"
)
sample_api_toolset = OpenAPIToolset(
    spec_str="...",  # Fill this with an OpenAPI spec string
    spec_str_type="yaml",
    auth_scheme=auth_scheme,
    auth_credential=auth_credential,
)
```

---

## 2. OAuth2 with AuthorizationCode Flow

```python
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from fastapi.openapi.models import OAuth2
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlows
from google.adk.auth import AuthCredential
from google.adk.auth import AuthCredentialTypes
from google.adk.auth import OAuth2Auth

auth_scheme = OAuth2(
    flows=OAuthFlows(
        authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl="https://accounts.google.com/o/oauth2/auth",
            tokenUrl="https://oauth2.googleapis.com/token",
            scopes={
                "https://www.googleapis.com/auth/calendar": "calendar scope"
            },
        )
    )
)
auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.OAUTH2,
    oauth2=OAuth2Auth(
        client_id=YOUR_OAUTH_CLIENT_ID,
        client_secret=YOUR_OAUTH_CLIENT_SECRET
    ),
)

calendar_api_toolset = OpenAPIToolset(
    spec_str=google_calendar_openapi_spec_str,  # Fill this with an openapi spec
    spec_str_type='yaml',
    auth_scheme=auth_scheme,
    auth_credential=auth_credential,
)
```

---

## 3. Service Account — `service_account_dict_to_scheme_credential()`

```python
from google.adk.tools.openapi_tool.auth.auth_helpers import service_account_dict_to_scheme_credential
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

service_account_cred = json.loads(service_account_json_str)
auth_scheme, auth_credential = service_account_dict_to_scheme_credential(
    config=service_account_cred,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
sample_toolset = OpenAPIToolset(
    spec_str=sa_openapi_spec_str,  # Fill this with an openapi spec
    spec_str_type='json',
    auth_scheme=auth_scheme,
    auth_credential=auth_credential,
)
```

---

## 4. OpenID Connect — `OpenIdConnectWithConfig`

```python
from google.adk.auth.auth_schemes import OpenIdConnectWithConfig
from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes, OAuth2Auth
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

auth_scheme = OpenIdConnectWithConfig(
    authorization_endpoint=OAUTH2_AUTH_ENDPOINT_URL,
    token_endpoint=OAUTH2_TOKEN_ENDPOINT_URL,
    scopes=['openid', 'YOUR_OAUTH_SCOPES']
)
auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.OPEN_ID_CONNECT,
    oauth2=OAuth2Auth(
        client_id="...",
        client_secret="...",
    )
)

userinfo_toolset = OpenAPIToolset(
    spec_str=content,  # Fill in an actual spec
    spec_str_type='yaml',
    auth_scheme=auth_scheme,
    auth_credential=auth_credential,
)
```

---

## 5. Google API Toolsets — `configure_auth(client_id, client_secret)`

```python
# Example: Configuring Google Calendar Tools
from google.adk.tools.google_api_tool import calendar_tool_set

client_id = "YOUR_GOOGLE_OAUTH_CLIENT_ID.apps.googleusercontent.com"
client_secret = "YOUR_GOOGLE_OAUTH_CLIENT_SECRET"

# Use the specific configure method for this toolset type
calendar_tool_set.configure_auth(
    client_id=oauth_client_id, client_secret=oauth_client_secret
)

# agent = LlmAgent(..., tools=calendar_tool_set.get_tool('calendar_tool_set'))
```

---

## 6. Interactive OAuth Flow — Detecting the Auth Request (Journey 1, Step 1)

### Run agent and detect `adk_request_credential`

```python
# runner = Runner(...)
# session = await session_service.create_session(...)
# content = types.Content(...) # User's initial query

print("\nRunning agent...")
events_async = runner.run_async(
    session_id=session.id, user_id='user', new_message=content
)

auth_request_function_call_id, auth_config = None, None

async for event in events_async:
    # Use helper to check for the specific auth request event
    if (auth_request_function_call := get_auth_request_function_call(event)):
        print("--> Authentication required by agent.")
        # Store the ID needed to respond later
        if not (auth_request_function_call_id := auth_request_function_call.id):
            raise ValueError(f'Cannot get function call id from function call: {auth_request_function_call}')
        # Get the AuthConfig containing the auth_uri etc.
        auth_config = get_auth_config(auth_request_function_call)
        break  # Stop processing events for now, need user interaction

if not auth_request_function_call_id:
    print("\nAuth not required or agent finished.")
    # return  # Or handle final response if received
```

### Helper functions — `get_auth_request_function_call()` and `get_auth_config()`

```python
from google.adk.events import Event
from google.adk.auth import AuthConfig  # Import necessary type
from google.genai import types

def get_auth_request_function_call(event: Event) -> types.FunctionCall:
    # Get the special auth request function call from the event
    if not event.content or not event.content.parts:
        return
    for part in event.content.parts:
        if (
            part
            and part.function_call
            and part.function_call.name == 'adk_request_credential'
            and event.long_running_tool_ids
            and part.function_call.id in event.long_running_tool_ids
        ):
            return part.function_call

def get_auth_config(auth_request_function_call: types.FunctionCall) -> AuthConfig:
    # Extracts the AuthConfig object from the arguments of the auth request function call
    if not auth_request_function_call.args or not (auth_config := auth_request_function_call.args.get('authConfig')):
        raise ValueError(f'Cannot get auth config from function call: {auth_request_function_call}')
    if isinstance(auth_config, dict):
        auth_config = AuthConfig.model_validate(auth_config)
    elif not isinstance(auth_config, AuthConfig):
        raise ValueError(f'Cannot get auth config {auth_config} is not an instance of AuthConfig.')
    return auth_config
```

---

## 7. Interactive OAuth Flow — Building the Redirect URI (Journey 1, Step 2)

```python
# (Continuing after detecting auth needed)

if auth_request_function_call_id and auth_config:
    # Get the base authorization URL from the AuthConfig
    base_auth_uri = auth_config.exchanged_auth_credential.oauth2.auth_uri

    if base_auth_uri:
        redirect_uri = 'http://localhost:8000/callback'  # MUST match your OAuth client app config
        # Append redirect_uri (use urlencode in production)
        auth_request_uri = base_auth_uri + f'&redirect_uri={redirect_uri}'
        # Redirect the end user to auth_request_uri or ask them to open it in their browser.
        # The auth provider will redirect the end user back to redirect_uri after login.
    else:
        print("ERROR: Auth URI not found in auth_config.")
        # Handle error
```

---

## 8. Interactive OAuth Flow — Sending Auth Response Back (Journey 1, Step 4)

```python
# (Continuing after user interaction / callback received)

    # Simulate getting the callback URL (e.g., from user paste or web handler)
    auth_response_uri = await get_user_input(
        f'Paste the full callback URL here:\n> '
    )
    auth_response_uri = auth_response_uri.strip()  # Clean input

    if not auth_response_uri:
        print("Callback URL not provided. Aborting.")
        return

    # Update the received AuthConfig with the callback details
    auth_config.exchanged_auth_credential.oauth2.auth_response_uri = auth_response_uri
    # Also include the redirect_uri used, as the token exchange might need it
    auth_config.exchanged_auth_credential.oauth2.redirect_uri = redirect_uri

    # Construct the FunctionResponse Content object
    auth_content = types.Content(
        role='user',  # Role can be 'user' when sending a FunctionResponse
        parts=[
            types.Part(
                function_response=types.FunctionResponse(
                    id=auth_request_function_call_id,   # Link to the original request
                    name='adk_request_credential',      # Special framework function name
                    response=auth_config.model_dump()   # Send back the *updated* AuthConfig
                )
            )
        ],
    )

    # --- Resume Execution ---
    print("\nSubmitting authentication details back to the agent...")
    events_async_after_auth = runner.run_async(
        session_id=session.id,
        user_id='user',
        new_message=auth_content,  # Send the FunctionResponse back
    )

    # --- Process Final Agent Output ---
    print("\n--- Agent Response after Authentication ---")
    async for event in events_async_after_auth:
        # Process events normally, expecting the tool call to succeed now
        print(event)
```

---

## 9. Full Journey 2 Example — `tools_and_agent.py`

```python
import os

from google.adk.auth.auth_schemes import OpenIdConnectWithConfig
from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes, OAuth2Auth
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.agents.llm_agent import LlmAgent

# --- Authentication Configuration ---
# This section configures how the agent will handle authentication using OpenID Connect (OIDC),
# often layered on top of OAuth 2.0.

# Define the Authentication Scheme using OpenID Connect.
# This object tells the ADK *how* to perform the OIDC/OAuth2 flow.
# It requires details specific to your Identity Provider (IDP), like Google OAuth, Okta, Auth0, etc.
# Note: Replace the example Okta URLs and credentials with your actual IDP details.
# All following fields are required, and available from your IDP.
auth_scheme = OpenIdConnectWithConfig(
    # The URL of the IDP's authorization endpoint where the user is redirected to log in.
    authorization_endpoint="https://your-endpoint.okta.com/oauth2/v1/authorize",
    # The URL of the IDP's token endpoint where the authorization code is exchanged for tokens.
    token_endpoint="https://your-token-endpoint.okta.com/oauth2/v1/token",
    # The scopes (permissions) your application requests from the IDP.
    # 'openid' is standard for OIDC. 'profile' and 'email' request user profile info.
    scopes=['openid', 'profile', "email"]
)

# Define the Authentication Credentials for your specific application.
# This object holds the client identifier and secret that your application uses
# to identify itself to the IDP during the OAuth2 flow.
# !! SECURITY WARNING: Avoid hardcoding secrets in production code. !!
# !! Use environment variables or a secret management system instead. !!
auth_credential = AuthCredential(
  auth_type=AuthCredentialTypes.OPEN_ID_CONNECT,
  oauth2=OAuth2Auth(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
  )
)

# --- Toolset Configuration from OpenAPI Specification ---
# This section defines a sample set of tools the agent can use, configured with Authentication
# from steps above.
# This sample set of tools use endpoints protected by Okta and requires an OpenID Connect flow
# to acquire end user credentials.
with open(os.path.join(os.path.dirname(__file__), 'spec.yaml'), 'r') as f:
    spec_content = f.read()

userinfo_toolset = OpenAPIToolset(
   spec_str=spec_content,
   spec_str_type='yaml',
   # ** Crucially, associate the authentication scheme and credentials with these tools. **
   # This tells the ADK that the tools require the defined OIDC/OAuth2 flow.
   auth_scheme=auth_scheme,
   auth_credential=auth_credential,
)

# --- Agent Configuration ---
# Configure and create the main LLM Agent.
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='enterprise_assistant',
    instruction='Help user integrate with multiple enterprise systems, including retrieving user information which may require authentication.',
    tools=userinfo_toolset.get_tools(),
)

# --- Ready for Use ---
# The `root_agent` is now configured with tools protected by OIDC/OAuth2 authentication.
# When the agent attempts to use one of these tools, the ADK framework will automatically
# trigger the authentication flow defined by `auth_scheme` and `auth_credential`
# if valid credentials are not already available in the session.
# The subsequent interaction flow would guide the user through the login process and handle
# token exchanging, and automatically attach the exchanged token to the endpoint defined in
# the tool.
```

---

## 10. Full Journey 2 Example — `agent_cli.py`

```python
import asyncio
from dotenv import load_dotenv
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .helpers import is_pending_auth_event, get_function_call_id, get_function_call_auth_config, get_user_input
from .tools_and_agent import root_agent

load_dotenv()

agent = root_agent

async def async_main():
  """
  Main asynchronous function orchestrating the agent interaction and authentication flow.
  """
  # --- Step 1: Service Initialization ---
  # Use in-memory services for session and artifact storage (suitable for demos/testing).
  session_service = InMemorySessionService()
  artifacts_service = InMemoryArtifactService()

  # Create a new user session to maintain conversation state.
  session = session_service.create_session(
      state={},       # Optional state dictionary for session-specific data
      app_name='my_app',  # Application identifier
      user_id='user'      # User identifier
  )

  # --- Step 2: Initial User Query ---
  query = 'Show me my user info'
  print(f"user: {query}")

  # Format the query into the Content structure expected by the ADK Runner.
  content = types.Content(role='user', parts=[types.Part(text=query)])

  # Initialize the ADK Runner
  runner = Runner(
      app_name='my_app',
      agent=agent,
      artifact_service=artifacts_service,
      session_service=session_service,
  )

  # --- Step 3: Send Query and Handle Potential Auth Request ---
  print("\nRunning agent with initial query...")
  events_async = runner.run_async(
      session_id=session.id, user_id='user', new_message=content
  )

  # Variables to store details if an authentication request occurs.
  auth_request_event_id, auth_config = None, None

  # Iterate through the events generated by the first run.
  async for event in events_async:
    # Check if this event is the specific 'adk_request_credential' function call.
    if is_pending_auth_event(event):
      print("--> Authentication required by agent.")
      auth_request_event_id = get_function_call_id(event)
      auth_config = get_function_call_auth_config(event)
      # Pause here to get user input for authentication.
      break

  # If no authentication request was detected after processing all events, exit.
  if not auth_request_event_id or not auth_config:
      print("\nAuthentication not required for this query or processing finished.")
      return

  # --- Step 4: Manual Authentication Step (Simulated OAuth 2.0 Flow) ---
  # Define the Redirect URI. This *must* match one of the URIs registered
  # with the OAuth provider for your application.
  redirect_uri = 'http://localhost:8000/dev-ui'  # Example for local development

  # Retrieve the base authorization URI from the AuthConfig provided by ADK
  # and append the redirect_uri.
  # NOTE: A robust implementation would use urlencode and potentially add state, scope, etc.
  auth_request_uri = (
      auth_config.exchanged_auth_credential.oauth2.auth_uri
      + f'&redirect_uri={redirect_uri}'
  )

  print("\n--- User Action Required ---")
  auth_response_uri = await get_user_input(
      f'1. Please open this URL in your browser to log in:\n   {auth_request_uri}\n\n'
      f'2. After successful login and authorization, your browser will be redirected.\n'
      f'   Copy the *entire* URL from the browser\'s address bar.\n\n'
      f'3. Paste the copied URL here and press Enter:\n\n> '
  )

  # --- Step 5: Prepare Authentication Response for the Agent ---
  auth_config.exchanged_auth_credential.oauth2.auth_response_uri = auth_response_uri
  auth_config.exchanged_auth_credential.oauth2.redirect_uri = redirect_uri

  auth_content = types.Content(
      role='user',
      parts=[
          types.Part(
              function_response=types.FunctionResponse(
                  id=auth_request_event_id,
                  name='adk_request_credential',
                  response=auth_config.model_dump(),
              )
          )
      ],
  )

  # --- Step 6: Resume Execution with Authentication ---
  print("\nSubmitting authentication details back to the agent...")
  events_async = runner.run_async(
      session_id=session.id,
      user_id='user',
      new_message=auth_content,
  )

  print("\n--- Agent Response after Authentication ---")
  async for event in events_async:
    print(event)


if __name__ == '__main__':
  asyncio.run(async_main())
```

---

## 11. Full Journey 2 Example — `helpers.py`

Helper utilities: `is_pending_auth_event()`, `get_function_call_id()`, `get_function_call_auth_config()`

```python
from google.adk.auth import AuthConfig
from google.adk.events import Event
import asyncio


async def get_user_input(prompt: str) -> str:
  """
  Asynchronously prompts the user for input in the console.

  Uses asyncio's event loop and run_in_executor to avoid blocking the main
  asynchronous execution thread while waiting for synchronous `input()`.
  """
  loop = asyncio.get_event_loop()
  return await loop.run_in_executor(None, input, prompt)


def is_pending_auth_event(event: Event) -> bool:
  """
  Checks if an ADK Event represents a request for user authentication credentials.

  The ADK framework emits a specific function call ('adk_request_credential')
  when a tool requires authentication that hasn't been previously satisfied.

  Returns:
    True if the event is an 'adk_request_credential' function call, False otherwise.
  """
  return (
      event.content
      and event.content.parts
      and event.content.parts[0]
      and event.content.parts[0].function_call
      and event.content.parts[0].function_call.name == 'adk_request_credential'
  )


def get_function_call_id(event: Event) -> str:
  """
  Extracts the unique ID of the function call from an ADK Event.

  This ID is crucial for correlating a function *response* back to the specific
  function *call* that the agent initiated to request auth credentials.

  Raises:
    ValueError: If the function call ID cannot be found in the event structure.
  """
  if (
      event
      and event.content
      and event.content.parts
      and event.content.parts[0]
      and event.content.parts[0].function_call
      and event.content.parts[0].function_call.id
  ):
    return event.content.parts[0].function_call.id
  raise ValueError(f'Cannot get function call id from event {event}')


def get_function_call_auth_config(event: Event) -> AuthConfig:
  """
  Extracts the AuthConfig from an 'adk_request_credential' event.

  Client should populate necessary authentication details (like OAuth codes and
  state) into this AuthConfig and send it back to ADK to continue token exchange.

  Raises:
    ValueError: If the 'auth_config' argument cannot be found in the event.
  """
  if (
      event
      and event.content
      and event.content.parts
      and event.content.parts[0]
      and event.content.parts[0].function_call
      and event.content.parts[0].function_call.args
      and event.content.parts[0].function_call.args.get('auth_config')
  ):
    return AuthConfig(
          **event.content.parts[0].function_call.args.get('auth_config')
      )
  raise ValueError(f'Cannot get auth config from event {event}')
```

---

## 12. Custom FunctionTool Auth — `tool_context: ToolContext` Skeleton

```python
from google.adk.tools import FunctionTool, ToolContext
from typing import Dict

def my_authenticated_tool_function(param1: str, tool_context: ToolContext) -> dict:
    # ... your logic using the steps below ...
    pass

my_tool = FunctionTool(func=my_authenticated_tool_function)
```

---

## 13. Custom FunctionTool Auth — Step 1: Check Token Cache

```python
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Inside your tool function
TOKEN_CACHE_KEY = "my_tool_tokens"  # Choose a unique key
SCOPES = ["scope1", "scope2"]       # Define required scopes

creds = None
cached_token_info = tool_context.state.get(TOKEN_CACHE_KEY)
if cached_token_info:
    try:
        creds = Credentials.from_authorized_user_info(cached_token_info, SCOPES)
        if not creds.valid and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            tool_context.state[TOKEN_CACHE_KEY] = json.loads(creds.to_json())  # Update cache
        elif not creds.valid:
            creds = None  # Invalid, needs re-auth
            tool_context.state[TOKEN_CACHE_KEY] = None
    except Exception as e:
        print(f"Error loading/refreshing cached creds: {e}")
        creds = None
        tool_context.state[TOKEN_CACHE_KEY] = None

if creds and creds.valid:
    pass  # Skip to Step 5: Make Authenticated API Call
else:
    pass  # Proceed to Step 2...
```

---

## 14. Custom FunctionTool Auth — Step 2: `tool_context.get_auth_response()`

```python
# Use auth_scheme and auth_credential configured in the tool.
# exchanged_credential: AuthCredential | None

exchanged_credential = tool_context.get_auth_response(AuthConfig(
    auth_scheme=auth_scheme,
    raw_auth_credential=auth_credential,
))
# If exchanged_credential is not None, ADK has already exchanged the access token.
if exchanged_credential:
    access_token = exchanged_credential.oauth2.access_token
    refresh_token = exchanged_credential.oauth2.refresh_token
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri=auth_scheme.flows.authorizationCode.tokenUrl,
        client_id=auth_credential.oauth2.client_id,
        client_secret=auth_credential.oauth2.client_secret,
        scopes=list(auth_scheme.flows.authorizationCode.scopes.keys()),
    )
    # Cache the token in session state and call the API — skip to Step 5
```

---

## 15. Custom FunctionTool Auth — Step 3: `tool_context.request_credential()`

```python
# Use auth_scheme and auth_credential configured in the tool.

tool_context.request_credential(AuthConfig(
    auth_scheme=auth_scheme,
    raw_auth_credential=auth_credential,
))
return {'pending': True, 'message': 'Awaiting user authentication.'}

# By setting request_credential, ADK detects a pending authentication event.
# It pauses execution and asks the end user to log in.
```

---

## 16. Custom FunctionTool Auth — Step 5: Cache Credentials

```python
# Inside your tool function, after obtaining 'creds' (refreshed or newly exchanged)
tool_context.state[TOKEN_CACHE_KEY] = json.loads(creds.to_json())
print(f"DEBUG: Cached/updated tokens under key: {TOKEN_CACHE_KEY}")
# Proceed to Step 6 (Make API Call)
```

---

## 17. Custom FunctionTool Auth — Step 6: Make Authenticated API Call

```python
# Inside your tool function, using the valid 'creds' object
if not creds or not creds.valid:
    return {"status": "error", "error_message": "Cannot proceed without valid credentials."}

try:
    service = build("calendar", "v3", credentials=creds)  # Example
    api_result = service.events().list(...).execute()
    # Proceed to Step 7
except Exception as e:
    # Handle API errors (e.g., check for 401/403, maybe clear cache and re-request auth)
    print(f"ERROR: API call failed: {e}")
    return {"status": "error", "error_message": f"API call failed: {e}"}
```

---

## 18. Custom FunctionTool Auth — Step 7: Return Tool Result

```python
# Inside your tool function, after successful API call
processed_result = [...]  # Process api_result for the LLM
return {"status": "success", "data": processed_result}
```
