import requests
from llm.ollama_client import run_llm
from config import REGISTRY_URL
from logger import logger


def router_node(state):
    logger.info("[ROUTER] ===== ROUTER START =====")
    logger.info(f"[ROUTER] User input: {state['input']}")

    # 1. Discover agents from registry
    logger.info(f"[ROUTER] Querying registry at {REGISTRY_URL}/agents")
    response = requests.get(f"{REGISTRY_URL}/agents")
    response.raise_for_status()

    agents = response.json()
    logger.info(f"[ROUTER] Discovered {len(agents)} agents")

    if not agents:
        logger.warning("[ROUTER] No agents discovered from registry")
        state["routes"] = []
        return state

    # 2. Build agent description for planner
    agent_descriptions = []
    for agent in agents:
        desc = f"- {agent['agent_id']}: {', '.join(agent['capabilities'])}"
        agent_descriptions.append(desc)

    agent_block = "\n".join(agent_descriptions)

    # 3. Planner prompt
    system_prompt = f"""
You are a planner agent.

Your task:
- Read the user input
- Select which agents are needed
- Decide execution order

AVAILABLE AGENTS:
{agent_block}

RULES:
- Output ONLY comma-separated agent_ids
- No explanations
- No extra text
"""

    logger.info("[ROUTER] Sending candidate agents to planner LLM")

    plan_raw = run_llm(system_prompt, state["input"]).strip().lower()
    logger.info(f"[ROUTER] Raw planner output: {plan_raw}")

    # Extract valid agent_ids from registry
    valid_agent_ids = {a["agent_id"] for a in agents}

    raw_routes = [r.strip() for r in plan_raw.split(",") if r.strip()]

    # HARD FILTER: only allow registered agent_ids
    routes = [r for r in raw_routes if r in valid_agent_ids]

    if not routes:
        logger.warning("[ROUTER] Planner returned no valid agent_ids, defaulting to weather")
        routes = ["weather"]

    logger.info(f"[ROUTER] Final execution plan: {routes}")
    logger.info("[ROUTER] ===== ROUTER END =====")

    state["routes"] = routes
    return state
