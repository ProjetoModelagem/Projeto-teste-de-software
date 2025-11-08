import pytest

def _seed_minimal(client, n=80):
    a = client.post("/authors", json={"author_nm": "Perf"}).json()
    aid = a.get("author_id") or a.get("id")
    for i in range(n):
        client.post("/books", json={
            "title_nm": f"Book {i:03d}",
            "author_id": aid,
            "genre_nm": "Test",
            "year_nbr": 2000 + (i % 20),
        })

@pytest.mark.benchmark(min_rounds=1, disable_gc=True)
def test_benchmark_search_books(client, benchmark):
    _seed_minimal(client, n=80)
    def run():
        r = client.get("/books/search?author_nm=perf&order_by=title")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list) and len(data) >= 40
    # pedantic = controla rodadas/iterações (evita abrir conexões demais)
    benchmark.pedantic(run, rounds=5, iterations=1)
