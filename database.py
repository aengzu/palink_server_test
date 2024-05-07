
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# MySQL 데이터베이스 URL 설정
# 예: "mysql://username:password@localhost/mydatabase"
DATABASE_URL = "mysql+pymysql://root:0000@127.0.0.1:3306/test"
#'mysql+pymysql://root:0000@127.0.0.1:3306/test'

engine = create_engine(
    DATABASE_URL,
    echo=True,  # True로 설정하면 SQL 로그를 출력합니다.
    pool_size=5,  # 커넥션 풀의 사이즈
    max_overflow=2,  # 풀 사이즈 이상의 커넥션 요청을 허용하는 최대 수
    pool_timeout=30,  # 풀에서 커넥션을 얻기 위해 대기할 최대 초 수
    pool_recycle=1800  # 커넥션을 재활용하기 전 최대 유지 시간(초)
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
