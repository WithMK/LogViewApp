# LogView API

FastAPI를 사용한 로그 데이터 관리 시스템의 백엔드 서버입니다.

## 프로젝트 구조

```
LogViewApp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── cutter/
│   │   │       ├── __init__.py
│   │   │       ├── lot/
│   │   │       │   ├── __init__.py
│   │   │       │   └── lot.py
│   │   │       ├── alarm/
│   │   │       │   ├── __init__.py
│   │   │       │   └── alarm.py
│   │   │       └── bar/
│   │   │           ├── __init__.py
│   │   │           └── bar.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── base.py
│   │   └── database.py
│   ├── requirements.txt
│   └── .env
└── frontend/  # React 프론트엔드 프로젝트
```

## 설치 방법

1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
.\venv\Scripts\activate  # Windows
```

2. 필요한 패키지 설치
```bash
pip install -r backend/requirements.txt
```

3. 환경 변수 설정
`.env` 파일을 수정하여 MS SQL Server 연결 정보를 설정합니다.

## 실행 방법

```bash
cd backend
uvicorn app.main:app --reload
```

## API 문서

서버가 실행되면 다음 주소로 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 데이터베이스 모델

### Lot
- 로트 관리 모델
- 필드: lot_number, product_code, start_time, end_time 등

### Alarm
- 알람 관리 모델
- 필드: alarm_code, description, severity, occurred_at 등

### Bar
- Bar 데이터 모델
- 필드: machine_id, start_time, end_time, lot_id, product_id, recipe_id, bar_count, time_duration
