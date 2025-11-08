from fastapi.testclient import TestClient
from src.controllers.api import app

client = TestClient(app)

def test_create_entities_and_open_close_loan(client, unique_email):
    ra = client.post("/authors", json={"author_nm": "Machado", "country_nm": "BR"}).json()
    rb = client.post("/books", json={
        "title_nm": "Dom Casmurro",
        "author_id": ra.get("author_id") or ra.get("id"),
        "genre_nm": "Romance",
        "year_nbr": 1899
    }).json()
    rm = client.post("/members", json={"member_nm": "Capitu", "email_nm": unique_email}).json()

    # fluxo completo: abrir e fechar empréstimo
    loan = client.post("/loans/open", json={
        "member_id": rm.get("member_id") or rm.get("id"),
        "book_id": rb.get("book_id") or rb.get("id"),
        "days_nbr": 2
    }).json()
    assert (loan.get("loan_id") or loan.get("id")), loan

    closed = client.post(f"/loans/{loan.get('loan_id') or loan.get('id')}/close").json()
    assert closed.get("return_dt") is not None

def test_search_books_and_loans_status(client):
    # endpoints de consulta (não quebram e retornam algo)
    _ = client.get("/books/search?author_nm=machado&order_by=title")
    _ = client.get("/loans/status/active")