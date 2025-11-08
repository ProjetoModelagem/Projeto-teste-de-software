import pytest

def test_close_loan_twice_is_safe(client, unique_email):
    a = client.post("/authors", json={"author_nm": "Safe Close"}).json()
    b = client.post("/books", json={"title_nm": "CloseTwice", "author_id": a.get("author_id") or a.get("id")}).json()
    m = client.post("/members", json={"member_nm": "Closer", "email_nm": unique_email}).json()

    loan = client.post("/loans/open", json={
        "member_id": m.get("member_id") or m.get("id"),
        "book_id": b.get("book_id") or b.get("id"),
        "days_nbr": 1
    }).json()

    lid = loan.get("loan_id") or loan.get("id")
    r1 = client.post(f"/loans/{lid}/close")
    assert r1.status_code in (200, 201), r1.text

    r2 = client.post(f"/loans/{lid}/close")
    # Aceita 200 (idempotente) ou 400/409/422 (já fechado)
    assert r2.status_code in (200, 400, 409, 422)
