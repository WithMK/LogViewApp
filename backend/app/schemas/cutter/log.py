from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class LogBase(BaseModel):
    level: str = Field(..., max_length=50)
    message: str = Field(..., max_length=255)
    source: str = Field(..., max_length=50)

class LogCreate(LogBase):
    # 생성 시에는 id와 created_at은 DB에서 자동 생성되거나 기본값이 설정될 수 있음
    pass

class Log(LogBase):
    id: int
    created_at: datetime

    class ConfigDict: # Pydantic v2
        from_attributes = True # SQLAlchemy ORM 모델과 매핑을 위해 필요 (ORM mode)