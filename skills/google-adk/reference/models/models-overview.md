# AI Models for ADK agents

PythonTypescriptGoJava

Agent Development Kit (ADK) is designed for flexibility, allowing you to
integrate various Large Language Models (LLMs) into your agents. This section
details how to leverage Gemini and integrate other popular models effectively,
including those hosted externally or running locally.

ADK primarily uses two mechanisms for model integration:

1. **Direct String / Registry:** For models tightly integrated with Google Cloud,
   such as Gemini models accessed via Google AI Studio or Vertex AI, or models
   hosted on Vertex AI endpoints. You access these models by providing the model name or endpoint resource string and ADK's internal registry
   resolves this string to the appropriate backend client.

   * Gemini models
   * Claude models
   * Vertex AI hosted models
2. **Model connectors:** For broader compatibility, especially models
   outside the Google ecosystem or those requiring specific client
   configurations, such as models accessed via Apigee or LiteLLM. You instantiate a specific wrapper class, such as `ApigeeLlm` or
   `LiteLlm`, and pass this object as the `model` parameter
   to your `LlmAgent`.

   * Apigee models
   * LiteLLM models
   * Ollama model hosting
   * vLLM model hosting
   * LiteRT-LM model hosting