from fastapi import FastAPI
from pydantic import BaseModel
from graph import app_graph
import uuid

app = FastAPI()

class Request(BaseModel):
    input: str

@app.post("/agent")
def agent(req: Request):
    result = app_graph.invoke({
        "input": req.input,
        "routes": [],
        "output": ""
    })

    return {
        "request_id": str(uuid.uuid4())[:8],
        "routes": result["routes"],
        "output": result["output"]
    }

