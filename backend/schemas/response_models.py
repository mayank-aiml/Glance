from typing import Any, Dict, Optional
from pydantic import BaseModel

class SummaryResponse(BaseModel):
    summary: str
    metadata: Dict[str, Any] = {}
    detail: Optional[str] = None
