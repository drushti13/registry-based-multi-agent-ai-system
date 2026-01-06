import requests
from fastapi import FastAPI
from pydantic import BaseModel
from config import REGISTRY_URL
from logger import logger
from datetime import datetime

app = FastAPI()

# ---- Agent Identity ----
AGENT_ID = "weather"
CAPABILITIES = ["weather", "temperature", "humidity", "wind"]
ENDPOINT = "http://127.0.0.1:8002/agent"

# Mumbai coordinates
LATITUDE = 19.0760
LONGITUDE = 72.8777


class Request(BaseModel):
    input: str


# ---- AUTO REGISTRATION ----
@app.on_event("startup")
def register_with_registry():
    payload = {
        "agent_id": AGENT_ID,
        "capabilities": CAPABILITIES,
        "endpoint": ENDPOINT
    }

    logger.info("[WEATHER] Registering with registry")

    try:
        res = requests.post(
            f"{REGISTRY_URL}/register",
            json=payload,
            timeout=5
        )
        res.raise_for_status()
        logger.info("[WEATHER] Successfully registered")

    except Exception as e:
        logger.error(f"[WEATHER] Registry registration failed: {e}")


# ---- WEATHER API CALL ----
def fetch_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}"
        f"&longitude={LONGITUDE}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        "&timezone=Asia/Kolkata"
    )

    logger.info("[WEATHER] Fetching real-time weather from Open-Meteo")

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()["current"]


# ---- AGENT EXECUTION ----
@app.post("/agent")
def agent(req: Request):
    logger.info("[WEATHER] Request received")
    logger.info(f"[WEATHER] Input: {req.input}")

    try:
        data = fetch_weather()

        output = (
            "WEATHER (Mumbai)\n"
            f"Temperature: {data['temperature_2m']} °C\n"
            f"Humidity: {data['relative_humidity_2m']} %\n"
            f"Wind Speed: {data['wind_speed_10m']} km/h\n"
            f"Updated: {datetime.now().strftime('%H:%M IST')}"
        )

        logger.info("[WEATHER] Weather fetched successfully")
        return {"output": output}

    except Exception as e:
        logger.error(f"[WEATHER] Weather API failed: {e}")
        return {
            "output": "Weather service temporarily unavailable. Please try again later."
        }
