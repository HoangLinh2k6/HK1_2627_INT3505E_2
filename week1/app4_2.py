from flask import Flask, jsonify,request

app = Flask(__name__)

BOOKS = [
    {"id": "a1", "title": "A1"},
    {"id": "a2", "title": "A2"},
    {"id": "a3", "title": "A3"}
]

@app.route("/books", methods=["GET"])
def list_books():
    limit=int(request.args.get("limit", 10))
    q=request.args.get("q", "").strip().lower()
    items= [b for b in BOOKS if q in b["title"].lower()]
    return jsonify(items[:limit]), 200
if __name__ == '__main__':
    app.run(debug=True)