from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.cutter.base import BaseModel
from datetime import datetime

class Lot(BaseModel):
    __tablename__ = "lots"

    id = Column(Integer, primary_key=True, index=True)
    lot_number = Column(String(50), nullable=False)  # 로트 번호
    product_code = Column(String(50), nullable=False)  # 제품 코드
    start_time = Column(DateTime, default=datetime.utcnow)  # 시작 시간
    end_time = Column(DateTime)  # 종료 시간
    status = Column(String(20))  # 로트 상태 (예: 진행중, 완료, 중지)
    quantity = Column(Integer)  # 생산 수량
    yield_rate = Column(Float)  # 수율
    
    # 관계 정의
    alarms = relationship("Alarm", back_populates="lot")  # 알람 관계
    
    def __repr__(self):
        return f"<Lot(id={self.id}, lot_number={self.lot_number}, status={self.status})>"
