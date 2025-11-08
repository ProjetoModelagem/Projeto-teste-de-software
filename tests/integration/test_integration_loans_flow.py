def test_open_then_close_loan_flow(client, unique_email):
    a = client.post("/authors", json={"author_nm": "Le Guin"}).json()
    b = client.post("/books", json={
        "title_nm": "Earthsea",
        "author_id": a.get("author_id") or a.get("id"),
        "genre_nm": "Fantasy",
        "year_nbr": 1968
    }).json()
    m = client.post("/members", json={"member_nm": "Ursula", "email_nm": unique_email}).json()

    loan = client.post("/loans/open", json={
        "member_id": m.get("member_id") or m.get("id"),
        "book_id": b.get("book_id") or b.get("id"),
        "days_nbr": 7
    })
    assert loan.status_code in (200, 201), loan.text
    lid = loan.json().get("loan_id") or loan.json().get("id")

    closed = client.post(f"/loans/{lid}/close")
    assert closed.status_code in (200, 201), closed.text
    assert closed.json().get("return_dt") is not None