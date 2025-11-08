def test_author_create_idempotent(client):
    payload = {"author_nm": "Asimov", "country_nm": "US"}
    r1 = client.post("/authors", json=payload)
    assert r1.status_code in (200, 201), r1.text
    r2 = client.post("/authors", json=payload)
    assert r2.status_code in (200, 201), r2.text
