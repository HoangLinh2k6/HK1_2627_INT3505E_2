from flask import Flask
from flask.views import MethodView
from flask_smorest import Blueprint, Api
from marshmallow import Schema, fields

app = Flask(__name__)

app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

DB = [
    {"id" : 1, "cost": 1},
    {"id" : 2, "cost": 2},
]

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    cost = fields.Int(required=True)

blp = Blueprint("products", __name__, url_prefix="/products")

@blp.route("/")
class ProductsResource(MethodView):
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        """List products"""
        return DB

    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, new_data):
        """Add a new product"""
        new_data["id"] = len(DB) + 1
        DB.append(new_data)
        return new_data


api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(debug=True)