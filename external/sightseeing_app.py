import requests
from fastapi import FastAPI
from pydantic import BaseModel
from config import REGISTRY_URL
from logger import logger
import os

app = FastAPI()

# ---- Agent Identity ----
AGENT_ID = "sightseeing"
CAPABILITIES = ["sightseeing", "tourist", "places"]
ENDPOINT = "http://127.0.0.1:9001/agent"

# ---- OpenTripMap Config ----
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")  # set once in env
LATITUDE = 19.0760     # Mumbai
LONGITUDE = 72.8777
RADIUS_METERS = 5000


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

    logger.info("[SIGHTSEEING] Registering with registry")

    try:
        res = requests.post(
            f"{REGISTRY_URL}/register",
            json=payload,
            timeout=5
        )
        res.raise_for_status()
        logger.info("[SIGHTSEEING] Successfully registered")

    except Exception as e:
        logger.error(f"[SIGHTSEEING] Registry registration failed: {e}")


# ---- FETCH REAL-TIME SIGHTSEEING PLACES ----
def fetch_places():
    # Bounding box around Mumbai
    min_lon = 72.80
    min_lat = 18.90
    max_lon = 73.00
    max_lat = 19.30

    url = (
        "https://api.opentripmap.com/0.1/en/places/bbox"
        f"?lon_min={min_lon}"
        f"&lat_min={min_lat}"
        f"&lon_max={max_lon}"
        f"&lat_max={max_lat}"
        "&kinds=historic,architecture,cultural,urban_environment"
        "&limit=5"
        f"&apikey={OPENTRIPMAP_API_KEY}"
    )

    logger.info("[SIGHTSEEING] Fetching places from OpenTripMap")
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json().get("features", [])


    


# ---- AGENT EXECUTION ----
@app.post("/agent")
def agent(req: Request):
    logger.info("[SIGHTSEEING] Request received")
    logger.info(f"[SIGHTSEEING] Input: {req.input}")

    if not OPENTRIPMAP_API_KEY:
        logger.error("[SIGHTSEEING] Missing OPENTRIPMAP_API_KEY")
        return {
            "output": "Sightseeing service is not configured properly."
        }

    try:
        places = fetch_places()

        if not places:
            return {
                "output": "No sightseeing places found nearby at the moment."
            }

        lines = ["SIGHTSEEING (Mumbai)"]

        for idx, place in enumerate(places, start=1):
            name = place["properties"].get("name", "Unknown place")
            category = place["properties"].get("kinds", "").split(",")[0]
            lines.append(f"{idx}. {name} – {category.replace('_', ' ').title()}")

        logger.info("[SIGHTSEEING] Places fetched successfully")
        return {"output": "\n".join(lines)}

    except Exception as e:
        logger.error(f"[SIGHTSEEING] OpenTripMap API failed: {e}")
        return {
            "output": "Sightseeing service is temporarily unavailable."
        }
