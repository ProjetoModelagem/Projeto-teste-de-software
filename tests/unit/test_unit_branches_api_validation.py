from fastapi.testclient import TestClient
from src.controllers.api import app

client = TestClient(app)

def test_books_post_422_missing_required_field():
    r = client.post("/books", json={"title_nm": "SemAutor"})
    assert r.status_code == 422, r.text  # ramo 422

def test_members_post_422_missing_email():
    r = client.post("/members", json={"member_nm": "Zoe"})
    assert r.status_code == 422, r.text  # ramo 422

def test_books_get_405_or_200():
    r = client.get("/books")
    # alguns backends respondem 405, outros implementam 200; cobrimos ambos
    assert r.status_code in (200, 405), r.text  # ramo 405/handler

def test_unknown_route_404():
    r = client.get("/route-that-does-not-exist")
    assert r.status_code == 404  # ramo 404 global
