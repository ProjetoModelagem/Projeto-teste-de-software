def test_status_active_endpoint(client):
    r = client.get("/loans/status/active")
    assert r.status_code == 200
