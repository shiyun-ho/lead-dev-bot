# === Input Schema ===
from pydantic import BaseModel


class DesignPlanRequest(BaseModel):
    body: str