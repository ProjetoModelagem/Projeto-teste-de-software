import inspect
import pytest
from sqlalchemy import create_engine, inspect as sa_inspect
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.repositories.entities import (
    AuthorRepository, BookRepository, MemberRepository, LoanRepository
)

@pytest.fixture
def sa_session():
    """Sessão SQLAlchemy isolada, em memória, só para este teste (caixa-branca OO)."""
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, future=True)
    sess = Session()
    try:
        yield sess
    finally:
        sess.close()

def test_models_tables_exist(sa_session):
    """Valida que as tabelas mapeadas existem após o create_all."""
    inspector = sa_inspect(sa_session.get_bind())
    tables = set(inspector.get_table_names())
    # Sem depender dos nomes das classes, só da existência das tabelas
    for t in ("author", "book", "member", "loan"):
        assert t in tables, f"tabela {t} não criada"

def test_repositories_polymorphism_shared_interface(sa_session):
    """Todos os repositórios expõem a mesma interface mínima: add/get/delete."""
    repos = [
        AuthorRepository(sa_session),
        BookRepository(sa_session),
        MemberRepository(sa_session),
        LoanRepository(sa_session),
    ]
    required = {"add", "get", "delete"}  # no seu código é 'get', não 'get_by_id'
    for r in repos:
        methods = {n for n, _ in inspect.getmembers(r, predicate=inspect.ismethod)}
        assert required.issubset(methods), f"{type(r).__name__} não implementa {required}"
