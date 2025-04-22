from pydantic import BaseModel
from typing import Dict


class TaskRequest(BaseModel):
    type: str
    data: Dict
