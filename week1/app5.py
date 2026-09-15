from flask import Flask, jsonify

app = Flask(__name__)

ORDERS = {
    "a": {"id": "a", "status": "pending"},
    "b": {"id": "b", "status": "shipped"},
    "c": {"id": "c", "status": "delivered"}
}

@app.route("/orders/<id>", methods=["DELETE"])
def delete_order(id):
    order = ORDERS.get(id)
    if order is None:
        return jsonify({"error": "not found"}), 404
    if order["status"] in ["shipped", "delivered"]:
        return jsonify({"error": "cannot delete"}), 409
    ORDERS.pop(id, None)
    return "", 204
if __name__ == '__main__':
    app.run(debug=True)
    