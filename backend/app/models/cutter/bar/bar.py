from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

# database.py에서 정의된 Base를 임포트
from app.database import Base

class BarTable(Base): # 기존 BarTable 이름 유지, Pydantic과 구분
    __tablename__ = "Bar_Table" # 실제 MS SQL 테이블명과 일치해야 합니다.

    id = Column(Integer, primary_key=True, index=True)
    # 한글을 저장할 컬럼들은 MS SQL의 NVARCHAR에 대응하기 위해 String 사용 (pyodbc가 잘 처리함)
    machine_id = Column(String(50), nullable=False)  # MachineID
    start_time = Column(DateTime)                    # StartTime
    end_time = Column(DateTime)                      # EndTime
    lot_id = Column(String(50), nullable=False)      # LotID
    product_id = Column(String(50), nullable=False)  # ProductID
    recipe_id = Column(String(50), nullable=False)   # RecipeID
    bar_count = Column(Integer)                      # BarCount
    time_duration = Column(Float)                    # TimeDuration
    
    # 관계 정의 (Lot 모델이 있다면)
    # lot = relationship("Lot", foreign_keys=[lot_id], backref="bars") 
    # Lot 테이블이 명확히 정의되지 않아 주석 처리했습니다. 필요 시 주석 해제 후 Lot 모델도 정의하세요.

    def __repr__(self):
        return f"<BarTable(id={self.id}, machine_id={self.machine_id}, lot_id={self.lot_id})>"