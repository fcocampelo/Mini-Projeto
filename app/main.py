from datetime import datetime, timezone
from typing import TypedDict

from fastapi import FastAPI

from app.api.task_routes import router as task_router


class HealthResponse(TypedDict):
    status: str
    timestamp: str


app = FastAPI(title="Mini-Projeto API")
app.include_router(task_router)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
