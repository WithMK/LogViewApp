from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..base import BaseModel
from datetime import datetime

class BarTable(BaseModel):
    __tablename__ = "Bar_Table"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String(50), nullable=False)  # MachineID
    start_time = Column(DateTime)  # StartTime
    end_time = Column(DateTime)  # EndTime
    lot_id = Column(String(50), nullable=False)  # LotID
    product_id = Column(String(50), nullable=False)  # ProductID
    recipe_id = Column(String(50), nullable=False)  # RecipeID
    bar_count = Column(Integer)  # BarCount
    time_duration = Column(Float)  # TimeDuration
    
    # 관계 정의
    lot = relationship("Lot", foreign_keys=[lot_id], backref="bars")  # Lot 테이블과의 관계
    
    def __repr__(self):
        return f"<BarTable(id={self.id}, machine_id={self.machine_id}, lot_id={self.lot_id})>"
