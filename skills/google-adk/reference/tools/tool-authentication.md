> Source: https://google.github.io/adk-docs/tools-custom/authentication/
> Fetched: 2026-03-10

# Authenticating with Tools

Supported in ADK Python v0.1.0

Many tools need to access protected resources (like user data in Google Calendar, Salesforce records, etc.) and require authentication. ADK provides a system to handle various authentication methods securely.

The key components involved are:

1. **`AuthScheme`**: Defines *how* an API expects authentication credentials (e.g., as an API Key in a header, an OAuth 2.0 Bearer token). ADK supports the same types of authentication schemes as OpenAPI 3.0. To know more about what each type of credential is, refer to OpenAPI doc: Authentication. ADK uses specific classes like `APIKey`, `HTTPBearer`, `OAuth2`, `OpenIdConnectWithConfig`.
2. **`AuthCredential`**: Holds the *initial* information needed to *start* the authentication process (e.g., your application's OAuth Client ID/Secret, an API key value). It includes an `auth_type` (like `API_KEY`, `OAUTH2`, `SERVICE_ACCOUNT`) specifying the credential type.

The general flow involves providing these details when configuring a tool. ADK then attempts to automatically exchange the initial credential for a usable one (like an access token) before the tool makes an API call. For flows requiring user interaction (like OAuth consent), a specific interactive process involving the Agent Client application is triggered.

## Supported Initial Credential Types

- **API\_KEY:** For simple key/value authentication. Usually requires no exchange.
- **HTTP:** Can represent Basic Auth (not recommended/supported for exchange) or already obtained Bearer tokens. If it's a Bearer token, no exchange is needed.
- **OAUTH2:** For standard OAuth 2.0 flows. Requires configuration (client ID, secret, scopes) and often triggers the interactive flow for user consent.
- **OPEN\_ID\_CONNECT:** For authentication based on OpenID Connect. Similar to OAuth2, often requires configuration and user interaction.
- **SERVICE\_ACCOUNT:** For Google Cloud Service Account credentials (JSON key or Application Default Credentials). Typically exchanged for a Bearer token.

## Configuring Authentication on Tools

You set up authentication when defining your tool:

- **RestApiTool / OpenAPIToolset**: Pass `auth_scheme` and `auth_credential` during initialization.
- **GoogleApiToolSet Tools**: ADK has built-in 1st party tools like Google Calendar, BigQuery, etc. Use the toolset's specific method.
- **APIHubToolset / ApplicationIntegrationToolset**: Pass `auth_scheme` and `auth_credential` during initialization, if the API managed in API Hub / provided by Application Integration requires authentication.

> **WARNING**
>
> Storing sensitive credentials like access tokens and especially refresh tokens directly in the session state might pose security risks depending on your session storage backend (`SessionService`) and overall application security posture.
>
> - **`InMemorySessionService`:** Suitable for testing and development, but data is lost when the process ends. Less risk as it's transient.
> - **Database/Persistent Storage:** **Strongly consider encrypting** the token data before storing it in the database using a robust encryption library (like `cryptography`) and managing encryption keys securely (e.g., using a key management service).
> - **Secure Secret Stores:** For production environments, storing sensitive credentials in a dedicated secret manager (like Google Cloud Secret Manager or HashiCorp Vault) is the **most recommended approach**. Your tool could potentially store only short-lived access tokens or secure references (not the refresh token itself) in the session state, fetching the necessary secrets from the secure store when needed.

---

## Journey 1: Building Agentic Applications with Authenticated Tools

This section focuses on using pre-existing tools (like those from `RestApiTool/OpenAPIToolset`, `APIHubToolset`, `GoogleApiToolSet`) that require authentication within your agentic application. Your main responsibility is configuring the tools and handling the client-side part of interactive authentication flows (if required by the tool).

### 1. Configuring Tools with Authentication

When adding an authenticated tool to your agent, you need to provide its required `AuthScheme` and your application's initial `AuthCredential`.

**A. Using OpenAPI-based Toolsets (`OpenAPIToolset`, `APIHubToolset`, etc.)**

Pass the scheme and credential during toolset initialization. The toolset applies them to all generated tools. The following patterns are supported:

- **API Key** — Create a tool requiring an API Key using the `token_to_scheme_credential()` helper.
- **OAuth2** — Create a tool requiring OAuth2 using `OAuth2` + `OAuthFlowAuthorizationCode` configuration.
- **Service Account** — Create a tool requiring a Google Service Account using `service_account_dict_to_scheme_credential()`.
- **OpenID Connect** — Create a tool requiring OpenID Connect using `OpenIdConnectWithConfig`.

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

**B. Using Google API Toolsets (e.g., `calendar_tool_set`)**

These toolsets often have dedicated configuration methods. Use `configure_auth(client_id, client_secret)` to supply OAuth credentials.

> **Tip:** For how to create a Google OAuth Client ID & Secret, see the guide: Get your Google API Client ID.

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

The auth request flow (where tools are requesting auth credentials) is described in the ADK documentation.

### 2. Handling the Interactive OAuth/OIDC Flow (Client-Side)

If a tool requires user login/consent (typically OAuth 2.0 or OIDC), the ADK framework pauses execution and signals your **Agent Client** application. There are two cases:

- **Agent Client** application runs the agent directly (via `runner.run_async`) in the same process — e.g., a UI backend, CLI app, or Spark job.
- **Agent Client** application interacts with ADK's FastAPI server via `/run` or `/run_sse` endpoint. The FastAPI server may be on the same or a different server as the Agent Client application.

The second case is a special case of the first, because `/run` or `/run_sse` also invokes `runner.run_async`. The only differences are:

- Whether to call a Python function to run the agent (first case) or call a service endpoint (second case).
- Whether the result events are in-memory objects (first case) or serialized JSON strings in an HTTP response (second case).

The sections below focus on the first case; mapping to the second case is straightforward.

Here is the step-by-step process for your client application:

**Step 1: Run Agent & Detect Auth Request**

- Initiate the agent interaction using `runner.run_async`.
- Iterate through the yielded events.
- Look for a specific function call event whose function call has the special name `adk_request_credential`. This event signals that user interaction is needed. You can use helper functions to identify this event and extract necessary information. (For the second case, deserialize the event from the HTTP response.)

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

**Step 2: Redirect User for Authorization**

- Get the authorization URL (`auth_uri`) from the `auth_config` extracted in the previous step.
- **Crucially, append your application's** `redirect_uri` as a query parameter to this `auth_uri`. This `redirect_uri` must be pre-registered with your OAuth provider (e.g., Google Cloud Console, Okta admin panel).
- Direct the user to this complete URL (e.g., open it in their browser).

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

**Step 3: Handle the Redirect Callback (Client)**

- Your application must have a mechanism (e.g., a web server route at the `redirect_uri`) to receive the user after they authorize the application with the provider.
- The provider redirects the user to your `redirect_uri` and appends an `authorization_code` (and potentially `state`, `scope`) as query parameters.
- Capture the **full callback URL** from this incoming request.
- (This step happens outside the main agent execution loop, in your web server or equivalent callback handler.)

**Step 4: Send Authentication Result Back to ADK (Client)**

- Once you have the full callback URL (containing the authorization code), retrieve the `auth_request_function_call_id` and the `auth_config` object saved in Step 1.
- Set the captured callback URL into the `exchanged_auth_credential.oauth2.auth_response_uri` field. Also ensure `exchanged_auth_credential.oauth2.redirect_uri` contains the redirect URI you used.
- Create a `types.Content` object containing a `types.Part` with a `types.FunctionResponse`:
  - Set `name` to `"adk_request_credential"`. (Note: This is a special name for ADK to proceed with authentication. Do not use other names.)
  - Set `id` to the `auth_request_function_call_id` you saved.
  - Set `response` to the *serialized* (e.g., `.model_dump()`) updated `AuthConfig` object.
- Call `runner.run_async` **again** for the same session, passing this `FunctionResponse` content as the `new_message`.

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

> **Note: Authorization response with Resume feature**
>
> If your ADK agent workflow is configured with the Resume feature, you also must include the Invocation ID (`invocation_id`) parameter with the authorization response. The Invocation ID you provide must be the same invocation that generated the authorization request, otherwise the system starts a new invocation with the authorization response. If your agent uses the Resume feature, consider including the Invocation ID as a parameter with your authorization request, so it can be included with the authorization response.

**Step 5: ADK Handles Token Exchange & Tool Retry**

- ADK receives the `FunctionResponse` for `adk_request_credential`.
- It uses the information in the updated `AuthConfig` (including the callback URL containing the code) to perform the OAuth **token exchange** with the provider's token endpoint, obtaining the access token (and possibly refresh token).
- ADK internally makes these tokens available by setting them in the session state.
- ADK **automatically retries** the original tool call (the one that initially failed due to missing auth).
- This time, the tool finds the valid tokens (via `tool_context.get_auth_response()`) and successfully executes the authenticated API call.
- The agent receives the actual result from the tool and generates its final response to the user.

---

The auth response flow (where Agent Client sends back the auth response and ADK retries tool calling) is described in the ADK documentation.

## Journey 2: Building Custom Tools (`FunctionTool`) Requiring Authentication

This section focuses on implementing the authentication logic *inside* your custom Python function when creating a new ADK Tool. A `FunctionTool` is used as the example.

### Prerequisites

Your function signature *must* include `tool_context: ToolContext` (see [Function Tools Overview](function-tools-overview.md)). ADK automatically injects this object, providing access to state and auth mechanisms.

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

### Authentication Logic within the Tool Function

Implement the following steps inside your function:

**Step 1: Check for Cached & Valid Credentials**

Inside your tool function, first check if valid credentials (e.g., access/refresh tokens) are already stored from a previous run in this session. Credentials for the current session should be stored in `tool_context.invocation_context.session.state` (a dictionary of state). Check existence with `tool_context.invocation_context.session.state.get(credential_name, None)`.

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

**Step 2: Check for Auth Response from Client**

If Step 1 didn't yield valid credentials, check if the client just completed the interactive flow by calling `exchanged_credential = tool_context.get_auth_response()`. This returns the updated `exchanged_credential` object sent back by the client (containing the callback URL in `auth_response_uri`).

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

**Step 3: Initiate Authentication Request**

If no valid credentials (Step 1) and no auth response (Step 2) are found, the tool needs to start the OAuth flow. Define the `AuthScheme` and initial `AuthCredential` and call `tool_context.request_credential()`. Return a response indicating authorization is needed. By setting `request_credential`, ADK detects a pending authentication event, pauses execution, and asks the end user to log in.

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

**Step 4: Exchange Authorization Code for Tokens**

ADK automatically generates an OAuth authorization URL and presents it to your Agent Client application. Your Agent Client application should follow the same process described in Journey 1 to redirect the user to the authorization URL (with `redirect_uri` appended). Once the user completes the login flow and ADK extracts the authentication callback URL from Agent Client applications, it automatically parses the auth code and generates an auth token. At the next tool call, `tool_context.get_auth_response` in Step 2 will contain a valid credential to use in subsequent API calls.

**Step 5: Cache Obtained Credentials**

After successfully obtaining the token from ADK (Step 2) or if the token is still valid (Step 1), **immediately store** the new `Credentials` object in `tool_context.state` (serialized, e.g., as JSON) using your cache key.

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

**Step 6: Make Authenticated API Call**

Once you have a valid `Credentials` object (`creds` from Step 1 or Step 4), use it to make the actual call to the protected API using the appropriate client library (e.g., `googleapiclient`, `requests`). Pass the `credentials=creds` argument.

Include error handling, especially for `HttpError` 401/403, which might mean the token expired or was revoked between calls. If you get such an error, consider clearing the cached token (`tool_context.state.pop(...)`) and potentially returning the `auth_required` status again to force re-authentication.

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

**Step 7: Return Tool Result**

After a successful API call, process the result into a dictionary format that is useful for the LLM. Crucially, include a `status` field along with the data.

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*

### Full Code Example

The full working example for Journey 2 spans four files:

- **`tools_and_agent.py`** — defines `auth_scheme`, `auth_credential`, the `OpenAPIToolset`, and the `LlmAgent`.
- **`agent_cli.py`** — orchestrates the full async flow: initial query, auth request detection, user prompt for the callback URL, assembling the `FunctionResponse`, and resuming execution.
- **`helpers.py`** — utility functions: `is_pending_auth_event()`, `get_function_call_id()`, `get_function_call_auth_config()`, and the async `get_user_input()` helper.
- **`spec.yaml`** — the OpenAPI 3.0.1 spec for the example Okta-protected endpoint (`/okta-jwt-user-api`), including the `okta_oidc` security scheme.

> *Code examples: see [tool-authentication-python.md](tool-authentication-python.md), [tool-authentication-typescript.md](tool-authentication-typescript.md), [tool-authentication-go.md](tool-authentication-go.md), [tool-authentication-java.md](tool-authentication-java.md)*
