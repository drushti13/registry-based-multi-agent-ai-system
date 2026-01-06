from fastapi import FastAPI
from pydantic import BaseModel
from registry.registry_store import register_agent, get_agents
from logger import logger

app = FastAPI(title="Agent Registry")

class RegisterRequest(BaseModel):
    agent_id: str
    capabilities: list[str]
    endpoint: str

@app.post("/register")

def register(req: RegisterRequest):
    logger.info(
        f"[REGISTRY] Register request | agent_id={req.agent_id} | endpoint={req.endpoint}"
    )
    register_agent(req.dict())
    logger.info(f"[REGISTRY] Agent registered: {req.agent_id}")
    return {"status": "ok"}
@app.get("/agents")
def agents():
    logger.info("[REGISTRY] Agent list requested")
    agents = get_agents()
    logger.info(f"[REGISTRY] Returning {len(agents)} agents")
    return agents

