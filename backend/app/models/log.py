from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base # SQLAlchemy 2.0+에서는 declarative_base 사용
from datetime import datetime

# database.py에서 정의된 Base를 임포트
from app.database import Base

class Log(Base):
    __tablename__ = "Log_Table" # 실제 MS SQL 테이블명과 일치해야 합니다.

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(50), nullable=False)
    message = Column(String(255), nullable=False)
    source = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now) # 생성 시간 자동 기록

    def __repr__(self):
        return f"<Log(id={self.id}, level={self.level}, message={self.message})>"