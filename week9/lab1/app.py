from flask import Flask, send_from_directory
from blueprints.v1 import bp as v1_bp
from blueprints.v2 import bp as v2_bp
app = Flask(__name__)
app.register_blueprint(v1_bp, url_prefix="/api/v1")
app.register_blueprint(v2_bp, url_prefix="/api/v2")


@app.route("/openapi.yaml")
def openapi_spec():
    return send_from_directory(app.root_path, "openapi.yaml", mimetype="application/yaml")