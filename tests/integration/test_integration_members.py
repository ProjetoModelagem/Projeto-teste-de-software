def test_member_create_and_get(client, unique_email):
    r = client.post("/members", json={"member_nm": "Alice", "email_nm": unique_email})
    assert r.status_code in (200, 201), r.text
    m = r.json()
    assert (m.get("member_id") or m.get("id")), m

def test_member_validation_missing_email_422(client):
    r = client.post("/members", json={"member_nm": "Bob"})
    assert r.status_code == 422
