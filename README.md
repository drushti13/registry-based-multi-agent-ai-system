# Registry-Based Multi-Agent AI System

## Description

This project is a **Registry-Based Multi-Agent AI System** that demonstrates how independent AI agents can be dynamically discovered, intelligently routed, and safely orchestrated using modern agentic design patterns.

The system uses a **registry-based agent discovery service**, a **local LLM (Ollama)** for reasoning, and a **lightweight HTTP-based A2A (Agent-to-Agent) protocol** for communication. Agents run as isolated FastAPI services and are selected at runtime based on user intent.

---

## Features

- **Registry-Based Agent Discovery Service**
  - Agents self-register with a central registry at startup
  - Registry stores agent ID, capabilities, and endpoint
  - Router dynamically discovers agents at runtime (no hardcoding)

- **LLM-Based Intelligent Routing**
  - Local LLM (Ollama – Qwen 2.5) plans which agents are required
  - Routing is capability-driven and registry-validated
  - Prevents hallucinated agents or tools

- **A2A (Agent-to-Agent) Protocol**
  - Lightweight HTTP-based communication
  - Standard endpoint: `POST /agent`
  - JSON request/response contract
  - Agents run as independent network services

- **LangGraph Orchestration**
  - Router → Executor → End flow
  - Clear separation of planning and execution
  - Deterministic control with agentic reasoning

---

## Architecture & Agent Flow

```mermaid
flowchart TD
    User --> Orchestrator
    Orchestrator --> Router
    Router --> Registry
    Registry --> Router
    Router --> Executor
    Executor --> WeatherAgent
    Executor --> FoodAgent
    Executor --> SightseeingAgent
    WeatherAgent --> Executor
    FoodAgent --> Executor
    SightseeingAgent --> Executor
    Executor --> User
```
Tech Stack

Python

FastAPI – Registry, orchestrator, agents

LangGraph – Agent orchestration flow

Ollama – Local LLM reasoning

Requests – Inter-agent HTTP calls

Pydantic – Data validation

External APIs – Open-Meteo, OpenTripMap
