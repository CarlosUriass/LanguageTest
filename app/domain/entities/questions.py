from pydantic import BaseModel
from typing import Optional

class Questions(BaseModel):
    id: Optional[int] = None
    question: str