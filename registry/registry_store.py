AGENT_REGISTRY = {}

def register_agent(agent):
    AGENT_REGISTRY[agent["agent_id"]] = {
        "agent_id": agent["agent_id"],
        "capabilities": agent["capabilities"],
        "endpoint": agent["endpoint"],
        "status": "healthy"
    }

def get_agents():
    return list(AGENT_REGISTRY.values())
