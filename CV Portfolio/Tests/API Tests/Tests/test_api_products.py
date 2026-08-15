import requests

BASE_URL = "http://localhost:5000"

## ------------------------- TESTS FOR: /products --------------------------------- ##

# Test - Is API accessible?
def test_is_API_accessible():
    response = requests.get(f"{BASE_URL}/api/products")
    assert response.status_code == 200


# Test - Are products listed when the API is called?
def test_are_products_listed():
    response = requests.get(f"{BASE_URL}/api/products")
    assert response.status_code == 200

    products = response.json()
    assert len(products) > 0


# Test - Are all products listed when the API is called?
def test_are_all_products_listed():
    response = requests.get(f"{BASE_URL}/api/products")
    assert response.status_code == 200

    products = response.json()
    expected_count = 8

    assert len(products) == expected_count


# Test - Are expected fields listed for each product?
def test_product_contains_expected_fields():
    response = requests.get(f"{BASE_URL}/api/products")

    product = response.json()[0]

    assert "id" in product
    assert "name" in product
    assert "description" in product
    assert "price" in product
    assert "stock" in product
    assert "category" in product


## -------------------------- TESTS FOR: /products/<id> ----------------------------- ##

# Test - Can individual products be called?
def test_call_single_product():
    response = requests.get(f"{BASE_URL}/api/products/1")
    assert response.status_code == 200


# Test - Is only one product listed when?
def test_confirm_only_one_product_called():
    response = requests.get(f"{BASE_URL}/api/products/1")
    assert response.status_code == 200

    product_count = str(response.json()).count('{')
    assert product_count == 1


# Test - Is information correct for the product?
def test_confirm_data_for_single_product():
    response = requests.get(f"{BASE_URL}/api/products/1")
    assert response.status_code == 200

    product = response.json()

    assert product["category"] == "Accessories"
    assert product["description"] == "Compact mechanical keyboard with hot-swappable switches."
    assert product["id"] == 1
    assert product["name"] == "Mechanical Keyboard"
    assert product["price"] == 89.99
    assert product["stock"] == 25


# Test - Is 404 returned for invalid product number?
def test_get_nonexistent_product_returns_404():
    response = requests.get(f"{BASE_URL}/api/products/999999")
    assert response.status_code == 404
