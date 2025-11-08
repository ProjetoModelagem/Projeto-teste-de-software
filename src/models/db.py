from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..utils.settings import get_settings
from ..models.base import Base

_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(settings.database_url, echo=False, future=True)
    return _engine

def get_session() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal()

def init_db() -> None:
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
