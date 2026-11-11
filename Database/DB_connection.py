from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from Configuration.config import DATABASE_URL
from Security.JWTAuth import get_user_id
from fastapi import Depends


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_and_user_id(session_user_id: int = Depends(get_user_id()), db: Session = Depends(get_db)):
    db.info['session_user_id'] = session_user_id
    try:
        yield db
    finally:
        db.close()

