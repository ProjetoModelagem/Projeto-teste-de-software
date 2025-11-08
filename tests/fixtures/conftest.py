import os, tempfile, shutil
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.services.library import LibraryService

@pytest.fixture()
def tmp_session():
    tmpdir = tempfile.mkdtemp()
    try:
        url = f"sqlite:///{os.path.join(tmpdir, 'test.sqlite3')}"
        engine = create_engine(url, echo=False, future=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        yield Session()
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

@pytest.fixture()
def svc(tmp_session):
    return LibraryService(tmp_session)
