import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 데이터베이스 정보 가져오기
DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ODBC_DRIVER = os.getenv("DB_ODBC_DRIVER")

# MS SQL 연결 문자열 (pyodbc 사용)
SQLALCHEMY_DATABASE_URL = (
    f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/"
    f"{DB_DATABASE}?driver={DB_ODBC_DRIVER}"
)

# SQLAlchemy 엔진 생성
# echo=True를 설정하면 실행되는 모든 SQL 쿼리를 콘솔에 출력하여 디버깅에 유용합니다.
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 세션 메이커 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy ORM 모델의 기본 클래스 (모든 모델이 상속받음)
Base = declarative_base()

def init_db():
    """
    데이터베이스 초기화 함수.
    이 함수는 Base에 등록된 모든 모델에 대해 테이블이 존재하지 않으면 생성합니다.
    (MS SQL에 이미 테이블이 있다면, 이 함수는 테이블을 다시 생성하지 않습니다.)
    """
    Base.metadata.create_all(bind=engine)
    print("Database initialization checked.")