from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel
from datetime import datetime

class Log(BaseModel):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False)  # 로그 레벨 (INFO, ERROR 등)
    message = Column(String(500), nullable=False)  # 로그 메시지
    source = Column(String(100))  # 로그 발생 소스
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 정의
    lot = relationship("Lot", back_populates="logs")  # Lot 테이블과의 관계
    
    def __repr__(self):
        return f"<Log(id={self.id}, level={self.level}, message={self.message[:50]})>"
