# Agent Development Kit

Agent Development Kit (ADK) is a flexible and modular framework for **developing
and deploying AI agents**. While optimized for Gemini and the Google ecosystem,
ADK is **model-agnostic**, **deployment-agnostic**, and is built for
**compatibility with other frameworks**. ADK was designed to make agent
development feel more like software development, to make it easier for
developers to create, deploy, and orchestrate agentic architectures that range
from simple tasks to complex workflows.

News: ADK Python Skills released!

ADK Python development [Agent Skills](https://agentskills.io/)
allow you to code ADK agents quickly and more effectively with
AI-powered development environments. For more details, check out
the Coding with AI,
ADK Skills docs.

Get started:


\

`pip install google-adk`

\

`npm install @google/adk`

\

`go get google.golang.org/adk`

pom.xml

```
<dependency>
    <groupId>com.google.adk</groupId>
    <artifactId>google-adk</artifactId>
    <version>0.6.0</version>
</dependency>
```

build.gradle

```
dependencies {
    implementation 'com.google.adk:google-adk:0.6.0'
}
```

Start with Python
Start with TypeScript
Start with Go
Start with Java

---

## Learn more

[Watch "Introducing Agent Development Kit"!](https://www.youtube.com/watch?v=zgrOwow_uTQ)

* **Flexible Orchestration**

  ---

  Define workflows using workflow agents (`Sequential`, `Parallel`, `Loop`)
  for predictable pipelines, or leverage LLM-driven dynamic routing
  (`LlmAgent` transfer) for adaptive behavior.

  **Learn about agents**
* **Multi-Agent Architecture**

  ---

  Build modular and scalable applications by composing multiple specialized
  agents in a hierarchy. Enable complex coordination and delegation.

  **Explore multi-agent systems**
* **Rich Tool Ecosystem**

  ---

  Equip agents with diverse capabilities: use pre-built tools (Search, Code
  Exec), create custom functions, integrate 3rd-party libraries, or even use
  other agents as tools.

  **Browse tools and integrations**
* **Deployment Ready**

  ---

  Containerize and deploy your agents anywhere – run locally, scale with
  Vertex AI Agent Engine, or integrate into custom infrastructure using Cloud
  Run or Docker.

  **Deploy agents**
* **Built-in Evaluation**

  ---

  Systematically assess agent performance by evaluating both the final
  response quality and the step-by-step execution trajectory against
  predefined test cases.

  **Evaluate agents**
* **Building Safe and Secure Agents**

  ---

  Learn how to building powerful and trustworthy agents by implementing
  security and safety patterns and best practices into your agent's design.

  **Safety and Security**