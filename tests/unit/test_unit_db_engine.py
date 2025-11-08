from src.models import db


def test_db_session_creation():
    """Testa criação e fechamento de sessão"""
    session = db.get_session()
    assert session is not None
    session.close()


def test_db_engine_singleton():
    """Garante que o engine é único"""
    engine1 = db.get_engine()
    engine2 = db.get_engine()
    assert engine1 is engine2
