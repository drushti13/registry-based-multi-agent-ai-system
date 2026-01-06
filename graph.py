from langgraph.graph import StateGraph, END
from state import AgentState
from router.router import router_node
from config import REGISTRY_URL
from logger import logger
from llm.ollama_client import run_llm
import requests


# -------- LLM EXPLAINER (POST-PROCESSING) --------
def explain_weather(weather_text: str) -> str:
    prompt = """
You are a helpful assistant.
Summarize the weather in ONE short, friendly sentence.
Use natural human language.
No emojis. No markdown. No extra details.
"""
    logger.info("[EXPLAINER] Generating human-friendly weather explanation")
    return run_llm(prompt, weather_text).strip()


# -------- EXECUTOR --------
def executor_node(state: AgentState):
    logger.info("[EXECUTOR] ===== EXECUTION START =====")
    logger.info(f"[EXECUTOR] Planned routes: {state['routes']}")

    response = requests.get(f"{REGISTRY_URL}/agents")
    response.raise_for_status()

    agents = response.json()
    endpoint_map = {a["agent_id"]: a["endpoint"] for a in agents}

    outputs = []

    for agent_id in state["routes"]:
        endpoint = endpoint_map.get(agent_id)

        if not endpoint:
            logger.warning(f"[EXECUTOR] No endpoint found for agent: {agent_id}")
            continue

        logger.info(
            f"[EXECUTOR] Calling agent | id={agent_id} | endpoint={endpoint}"
        )

        try:
            res = requests.post(endpoint, json={"input": state["input"]})
            res.raise_for_status()
            agent_output = res.json().get("output", "")

            logger.info(
                f"[EXECUTOR] Response received from {agent_id} "
                f"(status={res.status_code})"
            )

            outputs.append(agent_output)

        except Exception as e:
            logger.error(
                f"[EXECUTOR] Failed calling agent {agent_id}: {e}"
            )

    combined_output = "\n\n".join(outputs)

    # -------- HUMAN FRIENDLY WEATHER EXPLANATION --------
    if state["routes"] == ["weather"] and combined_output:
        explanation = explain_weather(combined_output)
        state["output"] = explanation + "\n\n" + combined_output
    else:
        state["output"] = combined_output

    logger.info("[EXECUTOR] ===== EXECUTION END =====")
    return state


# -------- LANGGRAPH WIRING --------
graph = StateGraph(AgentState)

graph.add_node("router", router_node)
graph.add_node("executor", executor_node)

graph.set_entry_point("router")
graph.add_edge("router", "executor")
graph.add_edge("executor", END)

app_graph = graph.compile()
