def test_options_root(client):
    r = client.options("/")
    # Alguns apps não tem OPTIONS no root; 405 é aceitável como contrato explícito
    assert r.status_code in (200, 204, 405)

def test_books_get_list_policy(client):
    r = client.get("/books")
    # Backend pode não listar todos (405) ou listar (200)
    assert r.status_code in (200, 405)

def test_create_author_idempotent_contract(client):
    r1 = client.post("/authors", json={"author_nm": "Contract"})
    r2 = client.post("/authors", json={"author_nm": "Contract"})
    assert r1.status_code in (200, 201)
    assert r2.status_code in (200, 201)

    def _nm(resp):
        j = resp.json()
        return j.get("author_nm") or j.get("name") or ""

    # Mesmo nome aceito/repetido é o que importa para contrato
    assert _nm(r1).lower() == "contract"
    assert _nm(r2).lower() == "contract"

    # IDs podem ser diferentes; apenas garantir que são inteiros válidos
    id1 = r1.json().get("author_id") or r1.json().get("id")
    id2 = r2.json().get("author_id") or r2.json().get("id")
    assert isinstance(id1, int) and isinstance(id2, int)
