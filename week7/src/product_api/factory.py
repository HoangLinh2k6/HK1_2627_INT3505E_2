from flask import Flask
from src.product_api.config import DefaultConfig
from src.product_api.extensions import db, migrate
from src.product_api.errors import register_error_handlers
from src.product_api.api.products import products_bp
from src.product_api.health import health_bp
from src.product_api.api.orders import orders_bp

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or DefaultConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    register_error_handlers(app)
    app.register_blueprint(products_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(orders_bp)

    return app