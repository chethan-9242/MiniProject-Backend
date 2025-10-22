import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Build DATABASE_URL from .env if not provided directly
_DATABASE_URL = os.getenv("DATABASE_URL")
if not _DATABASE_URL:
    user = os.getenv("POSTGRES_USER", "postgres")
    pwd = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db   = os.getenv("POSTGRES_DB", "postgres")
    _DATABASE_URL = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"

engine = create_engine(_DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# FastAPI dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
