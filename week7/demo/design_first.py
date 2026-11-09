from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)

DB = [
    {"id": 1, "cost": 1},
    {"id": 2, "cost": 2},
]

class ProductInSchema(Schema):
    cost = fields.Int(required=True)

class ProductOutSchema(Schema):
    id = fields.Int()
    cost = fields.Int()

@app.route("/products", methods=["GET"])
def list_products():
    return jsonify(ProductOutSchema(many=True).dump(DB)), 200

@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    try:
        validated_data = ProductInSchema().load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    new_item = {
        "id": len(DB) + 1,
        "cost": validated_data["cost"]
    }
    DB.append(new_item)
    return jsonify(ProductOutSchema().dump(new_item)), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)