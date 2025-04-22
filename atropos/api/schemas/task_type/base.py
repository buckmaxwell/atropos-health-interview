from pydantic import BaseModel
from typing import Dict, Any


class TaskType(BaseModel):
    type: str
    description: str
    payload_schema: Dict[str, Any]
