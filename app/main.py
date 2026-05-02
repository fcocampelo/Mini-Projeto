from datetime import datetime, timezone
from typing import TypedDict

from fastapi import FastAPI


class HealthResponse(TypedDict):
    status: str
    timestamp: str


app = FastAPI(title="Mini-Projeto API")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
