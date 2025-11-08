def test_search_by_author_and_order_title(client):
    _ = client.get("/books/search?author_nm=frank&order_by=title")
