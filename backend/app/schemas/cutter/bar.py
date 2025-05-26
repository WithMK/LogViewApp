from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BarBase(BaseModel):
    machine_id: str = Field(..., max_length=50)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    lot_id: str = Field(..., max_length=50)
    product_id: str = Field(..., max_length=50)
    recipe_id: str = Field(..., max_length=50)
    bar_count: Optional[int] = None
    time_duration: Optional[float] = None

class BarCreate(BarBase):
    # 생성 시에는 id는 DB에서 자동 생성
    pass

class Bar(BarBase):
    id: int

    class ConfigDict: # Pydantic v2
        from_attributes = True # SQLAlchemy ORM 모델과 매핑을 위해 필요 (ORM mode)