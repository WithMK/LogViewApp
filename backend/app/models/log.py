from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from .base import BaseModel
from datetime import datetime

class Log(BaseModel):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(10), nullable=False)  # INFO, ERROR, WARN 등
    message = Column(Text, nullable=False)
    source = Column(String(100))  # 로그 발생 소스
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Log(id={self.id}, level={self.level}, message={self.message[:50]})>"
