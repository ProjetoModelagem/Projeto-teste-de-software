import logging
from src.utils.logging_setup import setup_logging


def test_logging_setup_idempotent():
    """Executa setup_logging duas vezes sem duplicar handlers"""
    setup_logging()
    before = len(logging.getLogger().handlers)
    setup_logging()
    after = len(logging.getLogger().handlers)
    assert after == before
    assert any(isinstance(h, logging.Handler) for h in logging.getLogger().handlers)
