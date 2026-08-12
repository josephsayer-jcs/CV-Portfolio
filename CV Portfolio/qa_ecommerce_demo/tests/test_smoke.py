import pytest
from app import create_app, db
from app.models import Product

@pytest.fixture()
def client(tmp_path):
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path / 'test.db'}"
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Product(
            name="Test Product",
            description="Test",
            price=10.0,
            stock=5,
            category="Test"
        ))
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_product_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Test Product" in response.data

def test_product_api(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert response.json[0]["name"] == "Test Product"
