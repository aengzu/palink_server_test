import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 DATABASE_URL을 가져옴
DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL="mysql://USER:PASSWORD@HOST:PORT/DATABASE"

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(
    DATABASE_URL,
    echo=True,  # True로 설정하면 SQL 로그를 출력합니다.
    pool_size=5,  # 커넥션 풀의 사이즈
    max_overflow=2,  # 풀 사이즈 이상의 커넥션 요청을 허용하는 최대 수
    pool_timeout=30,  # 풀에서 커넥션을 얻기 위해 대기할 최대 초 수
    pool_recycle=1800  # 커넥션을 재활용하기 전 최대 유지 시간(초)
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
