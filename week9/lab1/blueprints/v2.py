from flask import Blueprint, request
from .users_data import add_user, get_user

bp = Blueprint("v2", __name__)


@bp.route("/users/<int:uid>")
def get(uid):
    u = get_user(uid)
    if not u: return {"error": "nf"}, 404
    return {
        "id": uid,
        "first_name": u["first_name"],
        "last_name": u["last_name"],
        "email": u["email"]
    }, 200


@bp.route("/users", methods=["POST"])
def post():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return {"error": "Request body must be a JSON object"}, 400

    required = ("first_name", "last_name", "email")
    missing = [field for field in required if not isinstance(body.get(field), str) or not body[field].strip()]
    if missing:
        return {"error": "Missing or invalid fields", "fields": missing}, 400

    first_name = body["first_name"].strip()
    last_name = body["last_name"].strip()
    email = body["email"].strip()
    uid, user = add_user(first_name, last_name, email)

    return {
        "id": uid,
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"]
    }, 201