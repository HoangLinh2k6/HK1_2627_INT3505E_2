import pytest
from product_api.factory import create_app
from product_api.config import DefaultConfig
from product_api.extensions import db

class TestConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Dùng DB RAM để test nhanh[cite: 198, 218]

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()