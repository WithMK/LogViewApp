from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import SessionLocal, init_db
from .models.log import Log
from .schemas.log import Log, LogCreate

app = FastAPI(title="LogView API")

# CORS 설정 (React 프론트엔드와 통신을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 초기화는 첫 번째 요청 시점에만 실행되도록 수정
@app.on_event("startup")
async def startup_event():
    """서버 시작 시 데이터베이스 연결을 시도합니다."""
    try:
        init_db()
    except Exception as e:
        print(f"데이터베이스 초기화 실패: {str(e)}")
        # 데이터베이스가 없어도 서버는 계속 실행됩니다

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 연결을 정리합니다."""
    # 필요한 정리 작업 수행

# 의존성 주입: 데이터베이스 세션
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to LogView API"}

@app.get("/logs", response_model=List[Log])
async def read_logs(db: Session = Depends(get_db)):
    logs = db.query(Log).all()
    return logs

@app.post("/logs", response_model=Log)
async def create_log(log: LogCreate, db: Session = Depends(get_db)):
    db_log = Log(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@app.get("/logs/{log_id}", response_model=Log)
async def read_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(Log).filter(Log.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return log

@app.delete("/logs/{log_id}")
async def delete_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(Log).filter(Log.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(log)
    db.commit()
    return {"message": "Log deleted successfully"}
