import requests
from fastapi import FastAPI
from pydantic import BaseModel
from llm.ollama_client import run_llm
from config import REGISTRY_URL
from logger import logger

app = FastAPI()

AGENT_ID = "food"
CAPABILITIES = ["food", "street food", "restaurants"]
ENDPOINT = "http://127.0.0.1:8003/agent"

class Request(BaseModel):
    input: str

@app.on_event("startup")
def register():
    payload = {
        "agent_id": AGENT_ID,
        "capabilities": CAPABILITIES,
        "endpoint": ENDPOINT
    }
    requests.post(f"{REGISTRY_URL}/register", json=payload)
    logger.info("[FOOD] Registered with registry")

@app.post("/agent")

def agent(req: Request):
    logger.info("[FOOD] Request received")
    logger.info(f"[FOOD] Input: {req.input}")

    output = run_llm("Food agent prompt", req.input)

    logger.info("[FOOD] LLM completed")
    return {"output": output}
