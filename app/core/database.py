from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import redis
from app.core.settings import settings 

# SQLAlchemy setup
engine = create_engine(settings.postgres_url(), echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency injection para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redis client
redis_client = redis.Redis.from_url(settings.redis_url(), decode_responses=True)
