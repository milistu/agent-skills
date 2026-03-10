# Agents

PythonTypeScriptGoJava

In Agent Development Kit (ADK), an **Agent** is a self-contained execution unit designed to act autonomously to achieve specific goals. Agents can perform tasks, interact with users, utilize external tools, and coordinate with other agents.

The foundation for all agents in ADK is the `BaseAgent` class. It serves as the fundamental blueprint. To create functional agents, you typically extend `BaseAgent` in one of three main ways, catering to different needs – from intelligent reasoning to structured process control.


## Core Agent Categories

ADK provides distinct agent categories to build sophisticated applications:

1. **LLM Agents (`LlmAgent`, `Agent`)**: These agents utilize Large Language Models (LLMs) as their core engine to understand natural language, reason, plan, generate responses, and dynamically decide how to proceed or which tools to use, making them ideal for flexible, language-centric tasks. Learn more about LLM Agents...
2. **Workflow Agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`)**: These specialized agents control the execution flow of other agents in predefined, deterministic patterns (sequence, parallel, or loop) without using an LLM for the flow control itself, perfect for structured processes needing predictable execution. Explore Workflow Agents...
3. **Custom Agents**: Created by extending `BaseAgent` directly, these agents allow you to implement unique operational logic, specific control flows, or specialized integrations not covered by the standard types, catering to highly tailored application requirements. Discover how to build Custom Agents...

## Choosing the Right Agent Type

The following table provides a high-level comparison to help distinguish between the agent types. As you explore each type in more detail in the subsequent sections, these distinctions will become clearer.

| Feature | LLM Agent (`LlmAgent`) | Workflow Agent | Custom Agent (`BaseAgent` subclass) |
| --- | --- | --- | --- |
| **Primary Function** | Reasoning, Generation, Tool Use | Controlling Agent Execution Flow | Implementing Unique Logic/Integrations |
| **Core Engine** | Large Language Model (LLM) | Predefined Logic (Sequence, Parallel, Loop) | Custom Code |
| **Determinism** | Non-deterministic (Flexible) | Deterministic (Predictable) | Can be either, based on implementation |
| **Primary Use** | Language tasks, Dynamic decisions | Structured processes, Orchestration | Tailored requirements, Specific workflows |

## Agents Working Together: Multi-Agent Systems

While each agent type serves a distinct purpose, the true power often comes from combining them. Complex applications frequently employ multi-agent architectures where:

* **LLM Agents** handle intelligent, language-based task execution.
* **Workflow Agents** manage the overall process flow using standard patterns.
* **Custom Agents** provide specialized capabilities or rules needed for unique integrations.

Understanding these core types is the first step toward building sophisticated, capable AI applications with ADK.

## Extend Agent Capabilities

Beyond the core agent types, ADK allows you to significantly expand what your
agents can do through several key mechanisms:

* **AI Models**:
  Swap the underlying intelligence of your agents by integrating with
  different generative AI models from Google and other providers.
* **Artifacts**:
  Enable agents to create and manage persistent outputs like files, code, or
  documents that exist beyond the conversation lifecycle.
* **Pre-built tools and integrations**:
  Equip your agents with a wide array tools, plugins, and other integrations
  to interact with the world, including web sites, MCP tools, applications,
  databases, programming interfaces, and more.
* **Custom tools**:
  Create your own, task-specific tools for solving specific problems with
  precision and control.
* **Plugins**:
  Integrate complex, pre-packaged behaviors and third-party services directly
  into your agent's workflow.
* **Skills**:
  Use prebuilt or custom [Agent Skills](https://agentskills.io/) to extend
  agent capabilities in a way that works efficiently inside AI context window
  limits.
* **Callbacks**:
  Hook into specific events during an agent's execution lifecycle to add
  logging, monitoring, or custom side-effects without altering core agent
  logic.