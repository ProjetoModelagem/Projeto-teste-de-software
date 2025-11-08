import os
import contextlib
import importlib
import pytest

@pytest.fixture(scope="session")
def db_file(tmp_path_factory):
    d = tmp_path_factory.mktemp("it_db")
    return str(d / "integration.sqlite3")

@pytest.fixture(scope="session", autouse=True)
def _set_test_database(db_file):
    # Aponta a app para um arquivo SQLite isolado p/ integração
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"

    # Força recarregar módulos da app depois de setar o env
    for m in list(importlib.sys.modules.keys()):
        if m.startswith(("src.models", "src.utils", "src.repositories", "src.services", "src.controllers")):
            importlib.sys.modules.pop(m, None)
    yield

@pytest.fixture(scope="session")
def app(_set_test_database):
    # Importa a app já com DATABASE_URL de teste
    from src.controllers.api import app as _app
    return _app

@pytest.fixture(scope="session")
def _create_schema(app):
    # Cria as tabelas no banco de integração
    from src.models.base import Base
    try:
        # se seu db.py expõe engine
        from src.models.db import engine as _engine
        eng = _engine
    except Exception:
        # ou tem um get_engine()
        from src.models.db import get_engine
        eng = get_engine()

    Base.metadata.create_all(bind=eng)
    yield

@pytest.fixture(scope="session")
def client(app, _create_schema):
    # Usa contexto para disparar lifespan (startup/shutdown)
    from fastapi.testclient import TestClient
    with TestClient(app) as c:
        yield c

# Helpers
@pytest.fixture
def post_ok(client):
    def _post_ok(path: str, payload: dict, ok=(200, 201)):
        r = client.post(path, json=payload)
        assert r.status_code in ok, (path, r.status_code, r.text)
        return r.json()
    return _post_ok

@pytest.fixture
def get_ok(client):
    def _get_ok(path: str, ok=(200,)):
        r = client.get(path)
        assert r.status_code in ok, (path, r.status_code, r.text)
        return r.json()
    return _get_ok
