import os, sys, pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Garantir "import src"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.models.base import Base
from src.controllers.api import app


@pytest.fixture
def _db_override():
    """
    SQLite em memória isolado por teste e override de get_session usado nos endpoints FastAPI.
    """
    from src.models import db as db_module  # importa o mesmo símbolo usado nos endpoints

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, future=True)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    def _get_test_session():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[db_module.get_session] = _get_test_session
    try:
        yield
    finally:
        app.dependency_overrides.pop(db_module.get_session, None)


@pytest.fixture
def client(_db_override):
    """
    TestClient já usando o DB isolado por teste (para testes de API/integr.).
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def svc():
    """
    LibraryService com DB em memória (para unit tests ‘caixa-branca’ sem subir API).
    """
    from src.services.library import LibraryService

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = SessionLocal()
    try:
        yield LibraryService(db)
    finally:
        db.close()


@pytest.fixture
def unique_email():
    return f"u{uuid4().hex[:8]}@example.com"