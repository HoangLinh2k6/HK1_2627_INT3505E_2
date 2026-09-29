from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

POSTS = [{"id": 1, "title": "Bài viết mẫu"}]

class ProblemError(Exception):
    def __init__(
        self,
        title,
        detail,
        status=400,
        type_uri="about:blank",
        instance=None,
        extra=None,
    ):
        super().__init__()
        self.title = title
        self.detail = detail
        self.status = status
        self.type_uri = type_uri
        self.instance = (
            instance or request.path
        )
        self.extra = extra or {}

    def to_dict(self):
        problem = {
            "type": self.type_uri,
            "title": self.title,
            "status": self.status,
            "detail": self.detail,
            "instance": self.instance,
        }
        problem.update(self.extra)
        return problem

@app.errorhandler(ProblemError)
def handle_problem_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status
    response.headers["Content-Type"] = "application/problem+json"
    return response

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    problem = {
        "type": (
            f"https://api.example.com/probs/{e.name.lower().replace(' ', '-')}"
        ),
        "title": e.name,
        "status": e.code,
        "detail": e.description,
        "instance": request.path,
    }
    response = jsonify(problem)
    response.status_code = e.code
    response.headers["Content-Type"] = "application/problem+json"
    return response

@app.route("/blog/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if post is None:
        raise ProblemError(
            title="Resource Not Found",
            detail=f"No post found with ID = {post_id}",
            status=404,
            type_uri="https://api.blog.example/errors/not-found",
        )
    return jsonify(post), 200