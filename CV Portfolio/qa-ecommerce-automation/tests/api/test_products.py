import requests

BASE_URL = "http://localhost:5000"


def test_get_products_returns_success():
    response = requests.get(f"{BASE_URL}/api/products")

    assert response.status_code == 200


def test_get_products_returns_products():
    response = requests.get(f"{BASE_URL}/api/products")

    assert response.status_code == 200

    products = response.json()

    assert len(products) > 0


def test_product_contains_expected_fields():
    response = requests.get(f"{BASE_URL}/api/products")

    product = response.json()[0]

    assert "id" in product
    assert "name" in product
    assert "description" in product
    assert "price" in product
    assert "stock" in product
    assert "category" in product


def test_get_existing_product():
    response = requests.get(f"{BASE_URL}/api/products/1")

    assert response.status_code == 200

    product = response.json()

    assert product["id"] == 1


def test_get_nonexistent_product_returns_404():
    response = requests.get(f"{BASE_URL}/api/products/999999")

    assert response.status_code == 404
