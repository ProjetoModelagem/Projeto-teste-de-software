import pytest
from fastapi.testclient import TestClient
from src.controllers.api import app

client = TestClient(app)


@pytest.mark.parametrize("endpoint,payload", [
    ("/members", {"member_nm": "Incomplete"}),         # falta email
    ("/books", {"book_nm": ""}),                       # nome vazio
])
def test_api_post_invalid_payload(endpoint, payload):
    """Valida erro 400/422 em payloads inválidos"""
    resp = client.post(endpoint, json=payload)
    assert resp.status_code in (400, 422)


def test_api_get_not_found():
    """Valida 404 ao buscar ID inexistente"""
    resp = client.get("/members/999999")
    assert resp.status_code == 404


def test_api_method_not_allowed():
    """Valida 405 em método incorreto"""
    resp = client.delete("/books")  # rota espera id
    assert resp.status_code in (400, 405)
