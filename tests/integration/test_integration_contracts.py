def test_422_validation_error(client):
    r = client.post("/books", json={"title_nm": "SemAutor"})  # falta author_id
    assert r.status_code == 422

def test_405_method_not_allowed(client):
    r = client.post("/books/search")  # endpoint é GET
    assert r.status_code in (404, 405)
