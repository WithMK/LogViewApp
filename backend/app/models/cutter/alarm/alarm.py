from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.cutter.base import BaseModel
from datetime import datetime

class Alarm(BaseModel):
    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(Integer, ForeignKey("lots.id"))  # 로트 참조
    alarm_code = Column(String(20), nullable=False)  # 알람 코드
    description = Column(String(200))  # 알람 설명
    severity = Column(String(10))  # 심각도 (예: 낮음, 중간, 높음)
    occurred_at = Column(DateTime, default=datetime.utcnow)  # 발생 시간
    resolved_at = Column(DateTime)  # 해결 시간
    
    # 관계 정의
    lot = relationship("Lot", back_populates="alarms")  # 로트 관계
    
    def __repr__(self):
        return f"<Alarm(id={self.id}, alarm_code={self.alarm_code}, severity={self.severity})>"
