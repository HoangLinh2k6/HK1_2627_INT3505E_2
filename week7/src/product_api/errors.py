from flask import jsonify
from werkzeug.exceptions import HTTPException

class ApiError(Exception):
    """Base exception cho mọi lỗi nghiệp vụ."""
    status_code = 500
    code = "internal_error"

    def __init__(self, message="", status=None, code=None):
        super().__init__(message)
        self.message = message
        if status is not None:
            self.status_code = status
        if code is not None:
            self.code = code

class NotFound(ApiError):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404, code="not_found")

class Conflict(ApiError):
    def __init__(self, message="Conflict"):
        super().__init__(message, status_code=409, code="conflict")

class OutOfStock(ApiError):
    def __init__(self, message="Out of stock"):
        super().__init__(message, status_code=409, code="out_of_stock")

def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(err):
        return jsonify({"code": err.code, "message": err.message}), err.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(err):
        return jsonify({
            "code": err.name.lower().replace(" ", "_"),
            "message": err.description
        }), err.code

    @app.errorhandler(Exception)
    def handle_unhandled_error(err):
        app.logger.exception("Unhandled Exception")
        return jsonify({"code": "internal_error", "message": "Internal Server Error"}), 500