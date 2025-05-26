from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List, Optional
import logging
from datetime import datetime, timezone # timezone 추가

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 데이터베이스 관련 임포트
from .database import SessionLocal, init_db

# SQLAlchemy ORM 모델 임포트 (충돌 방지를 위해 `as` 사용)
from app.models.cutter.log import Log as LogModel
from app.models.cutter.bar.bar import BarTable as BarModel

# Pydantic 스키마 임포트 (충돌 방지를 위해 `as` 사용)
from app.schemas.cutter.log import Log as LogSchema, LogCreate as LogCreateSchema
from app.schemas.cutter.bar import Bar as BarSchema, BarCreate as BarCreateSchema

app = FastAPI(title="LogView API")

# CORS 설정 (React 프론트엔드와 통신을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버 주소. 배포 시 실제 도메인 추가
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], # OPTIONS 메서드 추가 (CORS Preflight)
    allow_headers=["*"],
    expose_headers=["*"], # 클라이언트가 접근할 수 있는 헤더
    max_age=600 # 10분 동안 CORS Preflight 결과를 캐시
)

# 데이터베이스 초기화 및 연결 테스트
@app.on_event("startup")
async def startup_event():
    logger.info("서버 시작 중...")
    try:
        db = SessionLocal()
        # 간단한 쿼리로 DB 연결 테스트
        result = db.execute(text("SELECT 1")).fetchone()
        logger.info(f"데이터베이스 연결 성공. 테스트 결과: {result}")
        
        # 데이터베이스 초기화 (테이블이 없으면 생성)
        init_db()
        logger.info("데이터베이스 초기화 확인 완료.")
    except Exception as e:
        logger.error(f"데이터베이스 연결/초기화 실패: {e}", exc_info=True)
        # 중요: DB 연결 실패 시 서버 시작을 중단하거나 적절히 알림
        # raise Exception("Database connection failed. Exiting.") # 필요하다면 서버 시작을 막을 수도 있습니다.
        logger.warning("데이터베이스 연결 실패로 인해 일부 기능이 제한될 수 있습니다.")
    finally:
        if 'db' in locals() and db:
            try:
                db.close()
            except Exception as e:
                logger.warning(f"데이터베이스 세션 닫기 실패: {e}")
    
    logger.info("서버가 성공적으로 시작되었습니다.")

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 연결을 정리합니다."""
    logger.info("서버 종료 중...")
    # 필요한 정리 작업 수행 (예: 리소스 해제, 세션 강제 종료 등)
    logger.info("서버 종료 완료.")

# 의존성 주입: 데이터베이스 세션
def get_db(): # 비동기 함수가 아니어도 FastAPI는 적절히 처리합니다. (단, ORM은 동기)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=dict)
async def root():
    """API 루트 엔드포인트."""
    return {"message": "Welcome to LogView API! Access /docs for API documentation."}

# --- Log API 엔드포인트 ---

@app.get("/logs", response_model=List[LogSchema])
async def read_logs(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """모든 로그 데이터를 조회합니다. (페이지네이션 지원)"""
    logs = db.query(LogModel).offset(skip).limit(limit).all()
    return logs

@app.post("/logs", response_model=LogSchema, status_code=status.HTTP_201_CREATED)
async def create_log(log: LogCreateSchema, db: Session = Depends(get_db)):
    """새로운 로그 데이터를 생성합니다."""
    # created_at 필드를 수동으로 설정 (스키마에 default 값이 없으므로)
    db_log = LogModel(**log.model_dump(), created_at=datetime.now(timezone.utc))
    try:
        db.add(db_log)
        db.commit()
        db.refresh(db_log) # 데이터베이스에서 자동 생성된 ID 등을 반영
        return db_log
    except Exception as e:
        db.rollback() # 오류 발생 시 롤백
        logger.error(f"로그 생성 중 오류 발생: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="로그 생성 실패")

@app.get("/logs/{log_id}", response_model=LogSchema)
async def read_log(log_id: int, db: Session = Depends(get_db)):
    """특정 로그 데이터를 조회합니다."""
    log = db.query(LogModel).filter(LogModel.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")
    return log

@app.delete("/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(log_id: int, db: Session = Depends(get_db)):
    """로그 데이터를 삭제합니다."""
    log = db.query(LogModel).filter(LogModel.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")
    
    try:
        db.delete(log)
        db.commit()
        return {"message": "Log deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"로그 삭제 중 오류 발생: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="로그 삭제 실패")

# --- Bar API 엔드포인트 ---

@app.get("/bars", response_model=List[BarSchema])
async def read_bars(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """모든 Bar 데이터를 조회합니다. (페이지네이션 지원)"""
    # 더미 데이터 반환
    return [
        BarSchema(
            id=1,
            machine_id="MACHINE1",
            lot_id="LOT123",
            product_id="PRODUCT1",
            recipe_id="RECIPE1",
            bar_count=10,
            time_duration=30.5
        ),
        BarSchema(
            id=2,
            machine_id="MACHINE2",
            lot_id="LOT456",
            product_id="PRODUCT2",
            recipe_id="RECIPE2",
            bar_count=15,
            time_duration=45.2
        )
    ]

@app.get("/bars/{bar_id}", response_model=BarSchema)
async def read_bar(bar_id: int, db: Session = Depends(get_db)):
    """특정 Bar 데이터를 조회합니다."""
    # 더미 데이터 반환
    return BarSchema(
        id=bar_id,
        machine_id="MACHINE1",
        lot_id="LOT123",
        product_id="PRODUCT1",
        recipe_id="RECIPE1",
        bar_count=10,
        time_duration=30.5
    )

@app.post("/bars", response_model=BarSchema, status_code=status.HTTP_201_CREATED)
async def create_bar(bar: BarCreateSchema, db: Session = Depends(get_db)):
    """새로운 Bar 데이터를 생성합니다."""
    # 더미 데이터 반환
    return BarSchema(
        id=3,
        machine_id=bar.machine_id,
        lot_id=bar.lot_id,
        product_id=bar.product_id,
        recipe_id=bar.recipe_id,
        bar_count=bar.bar_count,
        time_duration=bar.time_duration
    )

@app.put("/bars/{bar_id}", response_model=BarSchema)
async def update_bar(bar_id: int, bar: BarCreateSchema, db: Session = Depends(get_db)):
    """Bar 데이터를 업데이트합니다."""
    # 더미 데이터 반환
    return BarSchema(
        id=bar_id,
        machine_id=bar.machine_id,
        lot_id=bar.lot_id,
        product_id=bar.product_id,
        recipe_id=bar.recipe_id,
        bar_count=bar.bar_count,
        time_duration=bar.time_duration
    )

@app.delete("/bars/{bar_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bar(bar_id: int, db: Session = Depends(get_db)):
    """Bar 데이터를 삭제합니다."""
    # 더미 데이터 반환
    return {"message": "Bar deleted successfully"}