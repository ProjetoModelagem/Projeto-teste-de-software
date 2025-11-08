def test_book_create_and_search(client):
    a = client.post("/authors", json={"author_nm": "Herbert"}).json()
    r = client.post("/books", json={
        "title_nm": "Dune",
        "author_id": a.get("author_id") or a.get("id"),
        "genre_nm": "Sci-Fi",
        "year_nbr": 1965
    })
    assert r.status_code in (200, 201), r.text
    _ = client.get("/books/search?title_nm=dune&order_by=title")
