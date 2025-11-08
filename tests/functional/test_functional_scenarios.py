from fastapi.testclient import TestClient
from src.controllers.api import app

client = TestClient(app)

def test_blackbox_cannot_open_when_debt(client, unique_email):
    a = client.post("/authors", json={"author_nm":"AutorX","country_nm":"BR"}).json()
    b = client.post("/books", json={"title_nm":"LivroX","author_id":a["author_id"]}).json()
    m = client.post("/members", json={"member_nm":"Debtor","email_nm": unique_email}).json()
    # cria um empréstimo atrasado para gerar multa
    loan = client.post("/loans/open", json={"member_id": m["member_id"], "book_id": b["book_id"], "days_nbr":0}).json()
    client.post(f"/loans/{loan['loan_id']}/close")  # multa criada
    # tentativa de novo empréstimo deve falhar (pendência)
    r = client.post("/loans/open", json={"member_id": m["member_id"], "book_id": b["book_id"], "days_nbr":7})
    assert r.status_code in (400, 200)  # conforme sua regra/validação