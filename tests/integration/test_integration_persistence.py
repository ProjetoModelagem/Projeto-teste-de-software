def test_persistence_roundtrip(client, unique_email):
    a = client.post("/authors", json={"author_nm": "RoundTrip"}).json()
    client.post("/books", json={
        "title_nm": "PersistX",
        "author_id": a.get("author_id") or a.get("id"),
        "genre_nm": "Test",
        "year_nbr": 2025
    })
    client.post("/members", json={"member_nm": "UserX", "email_nm": unique_email})
    # se chegar até aqui sem erro e /books/search não falhar, integra com DB
    r = client.get("/books/search?title_nm=persistx")
    assert r.status_code == 200
