from flask import Flask, jsonify

app = Flask(__name__)

BOOKS = [{"id": "abc", "title": "ABC"}]

def find_by_id(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None

@app.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    book = find_by_id(book_id)
    if book is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(book), 200
@app.route("/item/<int:item_id>", methods=["GET"])
def get_item(item_id):
    return jsonify({"item_id": item_id}), 200
if __name__ == '__main__':
    app.run(debug=True)