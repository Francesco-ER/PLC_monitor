from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime


class IngestPayload(BaseModel):
  company: str = Field(..., min_length=1)
ts: float | datetime | int
values: Dict[str, Any]


class LiveSnapshot(BaseModel):
  company: str
ts: float | datetime
values: Dict[str, Any]
_ts: float | None = None # metadata interna (cuando se guardó en cache)