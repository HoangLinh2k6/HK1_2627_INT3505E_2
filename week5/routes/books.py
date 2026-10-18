from flask import Blueprint, jsonify, request
from models import db, Book, Category
from sqlalchemy import select, func
import json
import os
from jsonschema import validate, ValidationError

DEFAULT_LIMIT, MAX_LIMIT = 20, 100

book_bp = Blueprint('books', __name__, url_prefix='/api/v1/books')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "schemas", "book.json")
SCHEMA = json.load(open(SCHEMA_PATH))

@book_bp.get('')
def list_books():
    offset = request.args.get("offset", 0, type=int)
    limit = min(request.args.get("limit", DEFAULT_LIMIT, type=int), MAX_LIMIT)
    total = db.session.scalar(select(func.count(Book.id)))
    rows = db.session.scalars(
        select(Book).order_by(Book.id).offset(offset).limit(limit)
    ).all()
    return jsonify({
        "data": [b.to_dict() for b in rows],
        "pagination": {
            "offset": offset,
            "limit": limit,
            "total": total,
            "has_next": offset + limit < total
        }
    })

@book_bp.get('/<int:book_id>')
def get_book(book_id):
    if book_id <= 0:
        return jsonify({"error": "Invalid book ID"}), 400
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict())

@book_bp.post('')
def create_book():
    data = request.get_json()
    try:
        validate(instance=data, schema=SCHEMA)
    except ValidationError as e:
        return jsonify({
            "error": "Invalid data",
            "field": list(e.path),
            "details": e.message
        }), 400
    return jsonify({"message": "Book created successfully"}), 201