"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, app, sample_book.
"""

def test_get_books_empty(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json == []

def test_get_book_not_found(client):
    response = client.get("/books/9999")
    assert response.status_code == 404
    assert response.json["code"] == "NOT_FOUND"

def test_post_book_missing_title(client):
    response = client.post("/books", json={"author": "abc", "year": 2000})
    assert response.status_code == 400
    assert any(err["field"] == "title" for err in response.json["errors"])

def test_post_delete_get_book(client):
    delete_response = client.delete(f"/books/1")
    assert delete_response.status_code == 204

    get_response = client.get(f"/books/1")
    assert get_response.status_code == 404

def test_response_extra_field_blocked(client):
    response = client.post("/books", json={"title": "ABC", "author": "abc", "year": 2000, "abc": "xyz"})
    assert response.status_code == 400
