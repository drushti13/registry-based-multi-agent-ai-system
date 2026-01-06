import requests
from config import EXTERNAL_SIGHTSEEING_AGENT_URL
from logger import logger

def sightseeing_node(state):
    logger.info(
        f"[A2A CLIENT] Sending request to external agent: {EXTERNAL_SIGHTSEEING_AGENT_URL}"
    )

    payload = {"input": state["input"]}
    logger.info(f"[A2A CLIENT] Payload: {payload}")

    response = requests.post(
        EXTERNAL_SIGHTSEEING_AGENT_URL,
        json=payload,
        timeout=60
    )

    logger.info(
        f"[A2A CLIENT] Response status: {response.status_code}"
    )

    response.raise_for_status()

    data = response.json()
    logger.info("[A2A CLIENT] Response received from external agent")

    state["output"] = data["output"]
    return state
