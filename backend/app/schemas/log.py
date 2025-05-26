from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogBase(BaseModel):
    level: str
    message: str
    source: Optional[str] = None

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
